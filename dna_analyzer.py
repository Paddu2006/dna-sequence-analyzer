# ============================================
# DNA Sequence Analyzer v2.0
# Author: Padma Shree
# Features: Multi-sequence, GC content, base count,
#            complement, reverse complement,
#            bar chart, save to file
# ============================================

import matplotlib.pyplot as plt
from datetime import datetime

def validate_sequence(sequence):
    valid_bases = set("ATGCatgc")
    return all(base in valid_bases for base in sequence)

def count_bases(sequence):
    sequence = sequence.upper()
    return {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "G": sequence.count("G"),
        "C": sequence.count("C")
    }

def calculate_gc_content(sequence):
    sequence = sequence.upper()
    gc = sequence.count("G") + sequence.count("C")
    return round((gc / len(sequence)) * 100, 2)

def calculate_at_gc_ratio(sequence):
    sequence = sequence.upper()
    at = sequence.count("A") + sequence.count("T")
    gc = sequence.count("G") + sequence.count("C")
    if gc == 0:
        return "undefined"
    return round(at / gc, 2)

def get_complement(sequence):
    mapping = str.maketrans("ATGCatgc", "TACGtacg")
    return sequence.translate(mapping)

def get_reverse_complement(sequence):
    return get_complement(sequence)[::-1]

def plot_bases(sequence, label):
    bases = count_bases(sequence)
    colors = ["#4CAF50", "#2196F3", "#FF9800", "#E91E63"]
    plt.figure(figsize=(7, 5))
    bars = plt.bar(bases.keys(), bases.values(), color=colors, edgecolor="black", width=0.5)
    for bar, val in zip(bars, bases.values()):
        plt.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.2, str(val),
                 ha="center", va="bottom", fontweight="bold", fontsize=12)
    plt.title(f"Base Composition — {label}", fontsize=14, fontweight="bold")
    plt.xlabel("Nucleotide Base", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.ylim(0, max(bases.values()) + 3)
    gc = calculate_gc_content(sequence)
    plt.suptitle(f"GC Content: {gc}%", fontsize=11, color="gray")
    plt.tight_layout()
    filename = f"chart_{label.replace(' ', '_')}.png"
    plt.savefig(filename)
    print(f"   Chart saved as: {filename}")
    plt.show()

def analyze_single(sequence, label, results_log):
    sequence = sequence.strip().upper()
    print("\n" + "="*50)
    print(f"  Analyzing: {label}")
    print("="*50)

    if not validate_sequence(sequence):
        msg = f"[{label}] Invalid sequence! Only A, T, G, C allowed."
        print(msg)
        results_log.append(msg)
        return

    bases     = count_bases(sequence)
    gc        = calculate_gc_content(sequence)
    ratio     = calculate_at_gc_ratio(sequence)
    comp      = get_complement(sequence)
    rev_comp  = get_reverse_complement(sequence)

    if gc < 40:
        interpretation = "AT-rich region"
    elif gc > 60:
        interpretation = "GC-rich region"
    else:
        interpretation = "Balanced GC content"

    # Display
    print(f"  Sequence            : {sequence}")
    print(f"  Length              : {len(sequence)} bases")
    print(f"  Base Counts         : A={bases['A']}  T={bases['T']}  G={bases['G']}  C={bases['C']}")
    print(f"  GC Content          : {gc}%")
    print(f"  AT/GC Ratio         : {ratio}")
    print(f"  Complement          : {comp}")
    print(f"  Reverse Complement  : {rev_comp}")
    print(f"  Interpretation      : {interpretation}")
    print("="*50)

    # Save to log
    results_log.append(f"""
Sequence            : {sequence}
Length              : {len(sequence)} bases
Base Counts         : A={bases['A']}  T={bases['T']}  G={bases['G']}  C={bases['C']}
GC Content          : {gc}%
AT/GC Ratio         : {ratio}
Complement          : {comp}
Reverse Complement  : {rev_comp}
Interpretation      : {interpretation}
{'-'*50}""")

    # Plot
    plot_bases(sequence, label)

def save_results(results_log):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"dna_results_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write("DNA SEQUENCE ANALYZER — RESULTS\n")
        f.write(f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
        f.write("="*50 + "\n")
        for entry in results_log:
            f.write(entry + "\n")
    print(f"\n Results saved to: {filename}")

# ── MAIN ──
if __name__ == "__main__":
    print("\n" + "="*50)
    print("    Welcome to DNA Sequence Analyzer v2.0")
    print("    Author: Padma Shree")
    print("="*50)

    results_log = []
    seq_count   = 1

    while True:
        print(f"\nEnter DNA sequence #{seq_count} (or type 'done' to finish):")
        user_input = input(">>> ").strip()

        if user_input.lower() == "done":
            break
        if user_input == "":
            print("Empty input, try again.")
            continue

        label = f"Sequence {seq_count}"
        analyze_single(user_input, label, results_log)
        seq_count += 1

    if results_log:
        save_results(results_log)
        print("\nThank you, Paddu! All sequences analyzed successfully!")
        print(f"Total sequences analyzed: {seq_count - 1}")
    else:
        print("\nNo valid sequences were entered.")