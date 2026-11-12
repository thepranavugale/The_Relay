# The_Relay – Final Project Report

## 1. What I built and why

The_Relay is a research-paper question-answering system that retrieves information from research papers and generates answers using an AI language model. I built it to explore how retrieval, answer generation, citation validation, and reliability mechanisms work together.

The system processes three research papers containing 111 pages and 1,116 text chunks. It uses TF-IDF retrieval, Groq API integration, citation validation, logging, retry handling, and rate limiting.

## 2. The real service and my stand-in

The real service is the Groq-hosted language model API (`openai/gpt-oss-120b`). The configurable StandInModel simulates responses, delays, and failures without making external API calls.

A single-request comparison recorded 1,001 ms for the stand-in and 2,333.31 ms for Groq. This is only one observation per service, not a general performance benchmark. The application uses non-streaming requests, so first-token latency was not measured.

## 3. Results

The combined `results/results.csv` contains 60 records: 45 stand-in load-test requests and 15 Groq quality-evaluation requests.

- Steady load: 10/10 successful; average 1.00 seconds.
- Burst load: 15/15 successful; average 1.00 seconds.
- Sustained concurrent load: 20/20 successful; average 2.01 seconds.
- Quality evaluation: 15/15 API requests completed successfully.
- Manual answer grading: 13 answers received grade 2 and 2 received grade 1; average 1.87/2.
- Citation validation: all 15 evaluated answers passed the citation-reference validation.
- Unit tests: 3/3 passed.

The manual grades are a small human-reviewed sample, not proof of overall factual accuracy.

## 4. Where the time goes

The stand-in load tests recorded approximately 1 second per request for steady and burst scenarios, and approximately 2 seconds for the sustained concurrent scenario. In the single service comparison, Groq took 2,333.31 ms and the stand-in took 1,001 ms.

Retrieval with top_k values of 2, 4, and 8 took an average of 1.541 ms, 1.675 ms, and 1.965 ms respectively. These are local retrieval timings; context size increased from approximately 1,902 to 7,490 characters. Character count is not API token count.

## 5. When a limit is hit

A local token-bucket simulation compared 10 requests/minute with 5 requests/minute. Four requests completed in approximately 12 seconds at the original limit and 24 seconds at the halved limit.

A separate daily-budget simulation accepted four requests consuming 1,000 simulated tokens and rejected the fifth. These experiments demonstrate local limit-handling logic; they do not measure actual Groq quota enforcement.

## 6. Retrieval: quality versus cost

I compared TF-IDF retrieval settings with top_k = 2, 4, and 8 across 15 query-setting combinations. Increasing top_k increased average retrieval time and context size. A larger context may provide more information but also increases the amount of text sent for generation.

The evaluation used manual answer grading, but it does not establish that one retrieval setting is universally best.

## 7. How this library will mislead a naive retriever

The three papers contain overlapping technical vocabulary. For example, a query about Transformer attention can retrieve chunks from Moshi and Dynamic Chunking ahead of the relevant Attention Is All You Need material.

This demonstrates a limitation of lexical TF-IDF retrieval: word overlap does not always mean conceptual relevance. Better ranking and semantic retrieval could improve this behavior.

## 8. Retries

The retry manager uses exponential backoff with jitter. A simulated test failed twice and succeeded on the third attempt. The Groq client is configured for two retries after the initial attempt.

Retries can help with temporary failures, but they add latency and should be limited to appropriate retryable errors.

## 9. What the person sees

The CLI application accepts a research question, retrieves relevant chunks, generates an answer, and displays citation-validation results. It handles empty input and allows the user to exit the application.

The citation validator checks whether cited paper and page references match retrieved material. It does not prove that the cited passage supports every claim.

## 10. What I'm unsure about, what I left out, what I learned

The load tests use a stand-in model and do not reproduce real provider overload. The service comparison contains only one request per service. First-token latency and actual input/output token counts were not captured. The sustained concurrent test does not implement a real provider-capacity rejection mechanism.

I learned that retrieval relevance, citation correctness, answer quality, latency, and rate limits are separate concerns. A system can return valid citations while still producing an incomplete or insufficiently supported answer.

## 11. Your feedback on Vaani

I would like to understand how Vaani evaluates answer quality, retrieval relevance, and reliability. I have not independently measured Vaani against The_Relay, so I cannot make a verified performance comparison.

## 12. How I worked with the assistant

I used the assistant for incremental implementation guidance, debugging, experiment planning, code review, and interpreting test results. I ran the commands locally, shared terminal outputs, and used the results to refine the project and its documentation.