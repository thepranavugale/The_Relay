
import pandas as pd

file_path = "results/manual_quality_grades.csv"

df = pd.read_csv(file_path)

corrections = {
    "Q01": (
        1,
        "The system correctly recognized that the retrieved context did not explain the main idea of the Transformer. It avoided generating unsupported information, but the question remained unanswered. Partial credit is appropriate because the system handled missing context safely."
    ),
    "Q02": (
        2,
        "Correctly explains self-attention advantages: computational efficiency, parallel processing, and shorter paths for learning long-range dependencies. Claims are supported by Attention Is All You Need, pages 2 and 6."
    ),
    "Q03": (
        2,
        "Correctly defines scaled dot-product attention using queries, keys, and values. Explains the QK transpose operation, scaling by the square root of key dimension, softmax, and weighted sum of values. Supported by Attention Is All You Need, page 4."
    ),
    "Q04": (
        2,
        "Correctly explains that multi-head attention allows the model to attend to multiple representation subspaces simultaneously. Describes parallel heads, concatenation, and projection. Supported by Attention Is All You Need, page 5."
    ),
    "Q05": (
        2,
        "Correctly explains why positional encoding is required when Transformers do not use recurrence or convolution. Describes adding positional vectors to embeddings and the sinusoidal encoding approach. Supported by Attention Is All You Need, page 6."
    ),
    "Q06": (
        1,
        "The answer describes the encoder configuration reported in the Moshi paper, including layers, attention heads, positional encoding, causal masking, and feed-forward components. However, it focuses on a specific Moshi implementation rather than clearly explaining the general Transformer encoder workflow. Partially correct but incomplete."
    ),
    "Q07": (
        2,
        "Correctly explains the Transformer's decoder structure, including masked self-attention, encoder-decoder cross-attention, and position-wise feed-forward networks. Also explains autoregressive generation and how the decoder uses encoder representations. Supported by Attention Is All You Need, pages 3 and 5."
    ),
    "Q08": (
        2,
        "Correctly explains that residual connections preserve information and support gradient flow, while layer normalization helps stabilize the network. The explanation is supported by the retrieved Transformer paper context."
    ),
    "Q09": (
        2,
        "Correctly compares recurrent models and self-attention in terms of sequential computation, parallelization, computational complexity, and long-range dependency paths. Supported by Attention Is All You Need, pages 2 and 6."
    ),
    "Q10": (
        2,
        "Correctly explains how Moshi combines text and speech through a unified sequence of text, semantic, and acoustic tokens. Also describes streaming speech and text generation. Supported by Moshi: A Speech-Text Foundation Model, pages 3 and 28."
    ),
    "Q11": (
        2,
        "Correctly explains Mimi as a neural audio codec that converts waveforms into discrete audio tokens and reconstructs audio. Describes its discrete bottleneck, residual vector quantization, semantic information, and streaming capability. Supported by Moshi: A Speech-Text Foundation Model, pages 3, 7, and 9."
    ),
    "Q12": (
        2,
        "Correctly defines residual vector quantization as sequential quantization of a vector and the residual left by earlier quantizers. Explains codebooks and its use in the Mimi audio codec. The answer includes a citation to Moshi: A Speech-Text Foundation Model, page 10."
    ),
    "Q13": (
        2,
        "Correctly explains dynamic chunking as a learned, tokenizer-free segmentation method. Describes jointly learning content-aware chunk boundaries and adapting sequence resolution. Supported by Dynamic Chunking for End-to-End Hierarchical Sequence Modeling, pages 3 and 33."
    ),
    "Q14": (
        2,
        "Correctly explains how hierarchical sequence modeling improves data efficiency through learned chunking, multi-resolution processing, and reduced sequence length. Includes reported benchmark improvements from the Dynamic Chunking paper, page 4."
    ),
    "Q15": (
        2,
        "Correctly discusses challenges in processing long sequences, including computational and memory costs, quadratic attention complexity, and long-range connectivity limitations. Supported by the Dynamic Chunking paper and Attention Is All You Need, page 7."
    )
}

for question_id, (grade, note) in corrections.items():
    mask = df["question_id"] == question_id
    df.loc[mask, "manual_grade"] = grade
    df.loc[mask, "review_notes"] = note

df.to_csv(file_path, index=False)

print("Manual quality grades and review notes updated.")
print("\nUpdated grade distribution:")
print(df["manual_grade"].value_counts().sort_index())

print("\nAverage score:", round(df["manual_grade"].mean(), 2), "/ 2")
print("Total questions:", len(df))
print("Missing grades:", df["manual_grade"].isna().sum())
