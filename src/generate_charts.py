import matplotlib.pyplot as plt

def main():
    architectures = ['Cascade Router\n(C++ / ONNX)', 'Python Proxy\n(e.g., LiteLLM)', 'SaaS Router\n(Network Hop)', 'LLM-as-a-Judge\n(Zero-Shot)']
    latencies_ms = [4.6, 65.0, 180.0, 850.0]

    # Use default light style for academic papers
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    # Custom colors: Highlight Cascade in brand blue, others in dark gray
    colors = ['#0ea5e9', '#4b5563', '#4b5563', '#4b5563']

    bars = ax.bar(architectures, latencies_ms, color=colors, width=0.6)

    # Add data labels on top of the bars (dark text)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + (yval * 0.05) + 5, 
                f"{yval} ms", ha='center', va='bottom', 
                fontweight='bold', fontsize=11, color='#1f2937')

    # Formatting (dark text)
    ax.set_yscale('log')
    ax.set_ylabel('Routing Latency Overhead (ms) - Log Scale', fontsize=12, fontweight='bold', labelpad=15, color='#1f2937')
    ax.set_title('AI Routing Latency: Cascade vs. Industry Standards', fontsize=16, fontweight='bold', pad=20, color='#111827')
    
    # Clean up axes for a crisp look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#d1d5db')
    ax.spines['bottom'].set_color('#d1d5db')
    ax.tick_params(axis='x', colors='#374151')
    ax.tick_params(axis='y', colors='#374151')
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#d1d5db')

    # Save the high-res image with a solid white background
    output_path = 'docs/latency_chart.png'
    plt.tight_layout()
    
    # CRITICAL: Forces a solid white background instead of transparent
    plt.savefig(output_path, transparent=False, facecolor='white')
    print(f"Success! High-resolution chart saved to {output_path}")

if __name__ == "__main__":
    main()
