import pandas as pd
import numpy as np
from scapy.all import rdpcap, IP, TCP, UDP, ICMP
from typing import List, Dict
import os


class PCAPConverter:
    """Convert PCAP files to CSV format for analysis"""
    
    @staticmethod
    def pcap_to_csv(pcap_file: str, output_csv: str = None) -> pd.DataFrame:
        """
        Convert PCAP file to CSV with extracted features
        
        Args:
            pcap_file: Path to PCAP file
            output_csv: Optional path to save CSV
            
        Returns:
            DataFrame with extracted features
        """
        packets = rdpcap(pcap_file)
        data = []
        
        for packet in packets:
            if IP in packet:
                packet_info = {
                    'timestamp': float(packet.time),
                    'src_ip': packet[IP].src,
                    'dst_ip': packet[IP].dst,
                    'protocol': packet[IP].proto,
                    'length': len(packet),
                    'ttl': packet[IP].ttl,
                    'flags': 0,
                    'src_port': 0,
                    'dst_port': 0,
                }
                
                # TCP specific features
                if TCP in packet:
                    packet_info['src_port'] = packet[TCP].sport
                    packet_info['dst_port'] = packet[TCP].dport
                    packet_info['flags'] = int(packet[TCP].flags)
                    packet_info['protocol_name'] = 'TCP'
                
                # UDP specific features
                elif UDP in packet:
                    packet_info['src_port'] = packet[UDP].sport
                    packet_info['dst_port'] = packet[UDP].dport
                    packet_info['protocol_name'] = 'UDP'
                
                # ICMP
                elif ICMP in packet:
                    packet_info['protocol_name'] = 'ICMP'
                else:
                    packet_info['protocol_name'] = 'OTHER'
                
                data.append(packet_info)
        
        df = pd.DataFrame(data)
        
        if output_csv:
            df.to_csv(output_csv, index=False)
        
        return df


class DataPreprocessor:
    """Preprocess network traffic data for model training"""
    
    def __init__(self):
        self.feature_columns = [
            'protocol', 'length', 'ttl', 'flags', 
            'src_port', 'dst_port', 'time_delta'
        ]
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data for model training
        
        Args:
            df: Raw network traffic DataFrame
            
        Returns:
            Preprocessed DataFrame
        """
        df = df.copy()
        
        # Calculate time deltas
        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp')
            df['time_delta'] = df['timestamp'].diff().fillna(0)
        else:
            df['time_delta'] = 0
        
        # Handle missing values
        for col in self.feature_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0)
            else:
                df[col] = 0
        
        # Remove outliers (values beyond 3 standard deviations)
        for col in ['length', 'time_delta']:
            if col in df.columns:
                mean = df[col].mean()
                std = df[col].std()
                df[col] = df[col].clip(lower=mean - 3*std, upper=mean + 3*std)
        
        return df
    
    def extract_features(self, df: pd.DataFrame) -> np.ndarray:
        """
        Extract features for model input
        
        Args:
            df: Preprocessed DataFrame
            
        Returns:
            Feature array
        """
        feature_df = df[self.feature_columns].copy()
        
        # Normalize numerical features
        for col in ['length', 'time_delta']:
            if col in feature_df.columns:
                max_val = feature_df[col].max()
                if max_val > 0:
                    feature_df[col] = feature_df[col] / max_val
        
        return feature_df.values


def load_and_preprocess_data(file_path: str) -> tuple:
    """
    Load and preprocess data from CSV or PCAP file
    
    Args:
        file_path: Path to data file
        
    Returns:
        Tuple of (preprocessed_df, features_array)
    """
    preprocessor = DataPreprocessor()
    
    # Load data based on file extension
    if file_path.endswith('.pcap'):
        converter = PCAPConverter()
        df = converter.pcap_to_csv(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Use .pcap or .csv")
    
    # Preprocess
    df = preprocessor.preprocess(df)
    features = preprocessor.extract_features(df)
    
    return df, features
