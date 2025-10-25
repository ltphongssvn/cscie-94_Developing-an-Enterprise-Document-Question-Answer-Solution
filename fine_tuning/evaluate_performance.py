# fine_tuning/evaluate_performance.py
# Automated performance analysis for Azure OpenAI fine-tuning results

import pandas as pd
import matplotlib.pyplot as plt
import os


def analyze_results(csv_path="fine_tuning/results.csv"):
    """Analyze training results and detect overfitting."""

    df = pd.read_csv(csv_path)

    print("=" * 60)
    print("FINE-TUNING PERFORMANCE ANALYSIS")
    print("=" * 60)

    # Summary statistics
    print("\n1. TRAINING SUMMARY")
    print(f"   Total steps: {len(df)}")
    print(f"   Initial train loss: {df['train_loss'].iloc[0]:.4f}")
    print(f"   Final train loss: {df['train_loss'].iloc[-1]:.4f}")
    print(
        f"   Loss reduction: {(1 - df['train_loss'].iloc[-1]/df['train_loss'].iloc[0])*100:.2f}%"
    )

    print(f"\n   Initial validation loss: {df['valid_loss'].iloc[0]:.4f}")
    print(f"   Final validation loss: {df['valid_loss'].iloc[-1]:.4f}")
    print(
        f"   Loss reduction: {(1 - df['valid_loss'].iloc[-1]/df['valid_loss'].iloc[0])*100:.2f}%"
    )

    print(f"\n   Initial token accuracy: {df['train_mean_token_accuracy'].iloc[0]:.4f}")
    print(f"   Final token accuracy: {df['train_mean_token_accuracy'].iloc[-1]:.4f}")
    print(
        f"   Accuracy gain: {(df['train_mean_token_accuracy'].iloc[-1] - df['train_mean_token_accuracy'].iloc[0])*100:.2f}%"
    )

    # Overfitting detection
    print("\n2. OVERFITTING ANALYSIS")
    train_trend = df["train_loss"].iloc[-1] - df["train_loss"].iloc[-5]
    valid_trend = df["valid_loss"].iloc[-1] - df["valid_loss"].iloc[-5]

    if train_trend < 0 and valid_trend > 0:
        print("   ⚠️  WARNING: Overfitting detected!")
        print(f"   Train loss decreasing ({train_trend:.4f})")
        print(f"   Valid loss increasing ({valid_trend:.4f})")
    elif train_trend < 0 and valid_trend < 0:
        print("   ✅ GOOD: Both losses decreasing")
        print(f"   Train: {train_trend:.4f}, Valid: {valid_trend:.4f}")
    else:
        print("   ℹ️  Model converged")

    # Best checkpoint
    best_step = df["valid_loss"].idxmin()
    print("\n3. BEST CHECKPOINT")
    print(f"   Step: {best_step}")
    print(f"   Train loss: {df.loc[best_step, 'train_loss']:.4f}")
    print(f"   Valid loss: {df.loc[best_step, 'valid_loss']:.4f}")
    print(f"   Accuracy: {df.loc[best_step, 'train_mean_token_accuracy']:.4f}")

    # Generate plots
    print("\n4. GENERATING VISUALIZATIONS")
    generate_plots(df)
    print("   ✅ Saved: fine_tuning/loss_curves.png")
    print("   ✅ Saved: fine_tuning/accuracy_plot.png")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)


def generate_plots(df):
    """Create loss and accuracy plots."""

    # Loss curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(df["step"], df["train_loss"], label="Train Loss", marker="o", markersize=3)
    ax1.plot(df["step"], df["valid_loss"], label="Valid Loss", marker="s", markersize=3)
    ax1.set_xlabel("Step")
    ax1.set_ylabel("Loss")
    ax1.set_title("Training & Validation Loss")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Accuracy
    ax2.plot(
        df["step"],
        df["train_mean_token_accuracy"],
        label="Token Accuracy",
        marker="o",
        markersize=3,
        color="green",
    )
    ax2.set_xlabel("Step")
    ax2.set_ylabel("Accuracy")
    ax2.set_title("Token Accuracy Over Time")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("fine_tuning/loss_curves.png", dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    if os.path.exists("fine_tuning/results.csv"):
        analyze_results()
    else:
        print("❌ results.csv not found. Run download_results.py first.")
