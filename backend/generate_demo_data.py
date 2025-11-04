import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample network traffic data
n_samples = 1000
base_time = datetime.now().timestamp()

# Normal traffic (90% of data)
n_normal = 900
normal_data = {
    'timestamp': [base_time + i * 0.1 for i in range(n_normal)],
    'src_ip': [f"192.168.1.{np.random.randint(1, 255)}" for _ in range(n_normal)],
    'dst_ip': [f"10.0.0.{np.random.randint(1, 255)}" for _ in range(n_normal)],
    'protocol': np.random.choice([6, 17], n_normal),  # TCP=6, UDP=17
    'length': np.random.normal(500, 150, n_normal).clip(64, 1500).astype(int),
    'ttl': np.random.normal(64, 5, n_normal).clip(32, 128).astype(int),
    'flags': np.random.choice([2, 16, 18, 24], n_normal),  # Common TCP flags
    'src_port': np.random.randint(1024, 65535, n_normal),
    'dst_port': np.random.choice([80, 443, 22, 8080], n_normal),
    'protocol_name': np.random.choice(['TCP', 'UDP'], n_normal)
}

# Anomalous traffic (10% of data)
n_anomaly = 100
anomaly_data = {
    'timestamp': [base_time + (n_normal + i) * 0.1 for i in range(n_anomaly)],
    'src_ip': [f"172.16.{np.random.randint(0, 255)}.{np.random.randint(0, 255)}" for _ in range(n_anomaly)],
    'dst_ip': [f"192.168.1.{np.random.randint(1, 255)}" for _ in range(n_anomaly)],
    'protocol': np.random.choice([6, 17, 1], n_anomaly),  # Include ICMP=1
    'length': np.random.choice([64, 1500], n_anomaly),  # Extreme sizes
    'ttl': np.random.randint(1, 255, n_anomaly),  # Unusual TTL values
    'flags': np.random.randint(0, 255, n_anomaly),  # Unusual flags
    'src_port': np.random.randint(1, 65535, n_anomaly),
    'dst_port': np.random.randint(1, 65535, n_anomaly),  # Random ports instead of common ones
    'protocol_name': np.random.choice(['TCP', 'UDP', 'ICMP'], n_anomaly)
}

# Combine normal and anomalous data
df_normal = pd.DataFrame(normal_data)
df_anomaly = pd.DataFrame(anomaly_data)
df = pd.concat([df_normal, df_anomaly], ignore_index=True)

# Shuffle the data
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV
df.to_csv('../demo_data/sample_traffic.csv', index=False)

print(f"Generated {len(df)} samples ({n_normal} normal, {n_anomaly} anomalous)")
print(f"Saved to ../demo_data/sample_traffic.csv")
print(f"\nFirst few rows:")
print(df.head())
