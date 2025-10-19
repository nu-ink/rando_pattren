import time
import torch
import tensorflow as tf
import numpy as np

def benchmark_pytorch():
    """Benchmark GPU performance using PyTorch."""
    print("\n[+] Running PyTorch GPU benchmark...")

    if torch.cuda.is_available():
        device = torch.device("cuda")
        x = torch.randn(10000, 10000, device=device)
        
        start_time = time.time()
        for _ in range(10):
            torch.matmul(x, x)
        torch.cuda.synchronize()  # Ensure all operations are done
        end_time = time.time()

        print(f"    - PyTorch GPU Test: Completed in {end_time - start_time:.4f} seconds")
    else:
        print("[-] PyTorch GPU not available.")


def benchmark_tensorflow():
    """Benchmark GPU performance using TensorFlow."""
    print("\n[+] Running TensorFlow GPU benchmark...")

    if tf.config.list_physical_devices('GPU'):
        x = tf.random.normal([10000, 10000])
        
        start_time = time.time()
        for _ in range(10):
            _ = tf.linalg.matmul(x, x)
        tf.config.experimental_functions_run_eagerly(True)
        end_time = time.time()

        print(f"    - TensorFlow GPU Test: Completed in {end_time - start_time:.4f} seconds")
    else:
        print("[-] TensorFlow GPU not available.")


def run_gpu_benchmark():
    print("=== Starting GPU Benchmark ===")
    benchmark_pytorch()
    benchmark_tensorflow()
    print("================================")

if __name__ == "__main__":
    run_gpu_benchmark()
