# Index

_Derived by `./kb build`. Do not edit; edit the pages._

## Maps

- [[ai-curriculum]] — A prerequisite-ordered map from math foundations to LLM systems, safety and evaluation. (stub, low) · ai

## Concepts

- [[adam-and-modern-optimizers]] — Variants of gradient descent that adapt step sizes using the history of gradients. (stub, low) · ai
- [[ai-alignment]] — Making a system's behaviour match its designers' intended goals and values. (stub, low) · ai
- [[backpropagation]] — Efficiently computing the gradient of the loss for every parameter using the chain rule. (stub, low) · ai
- [[benchmark-contamination]] — Test data leaking into training data and inflating scores. (stub, low) · ai
- [[convolutional-neural-networks]] — Networks that share small filters across positions, well suited to images. (stub, low) · ai
- [[decoding-and-sampling]] — Choosing the next token from the model's distribution: greedy, temperature, top-k, top-p. (stub, low) · ai
- [[derivatives-and-gradients]] — How a function changes with its inputs; the basis for training by gradient descent. (stub, low) · science
- [[diffusion-models]] — Generating data by learning to reverse a gradual noising process. (stub, low) · ai
- [[direct-preference-optimization]] — Optimising a model directly on preference pairs without a separate reward model. (stub, low) · ai
- [[embeddings]] — Dense vectors representing discrete items such as words, so that similar items lie close together. (stub, low) · ai
- [[entropy-and-cross-entropy]] — Measures of uncertainty and of the gap between two distributions; cross-entropy is the standard loss for classification and language models. (stub, low) · science
- [[evaluating-llms]] — Measuring model quality with benchmarks, human judgment and model-based graders, and the pitfalls of each. (stub, low) · ai
- [[gradient-descent]] — Iteratively adjusting parameters in the direction that reduces the loss. (stub, low) · ai
- [[hallucination]] — A model producing fluent but false or unsupported statements. (stub, low) · ai
- [[in-context-learning]] — A model adapting to a task from examples in its prompt without any weight updates. (stub, low) · ai
- [[kv-cache]] — Caching attention keys and values so earlier tokens are not recomputed during generation. (stub, low) · ai
- [[language-modeling]] — Training a model to predict the next token; the pretraining objective of most LLMs. (stub, low) · ai
- [[linear-algebra-for-ml]] — Vectors, matrices and their operations: the language in which neural networks are written. (stub, low) · science
- [[llm-agents]] — Systems where a model loops over planning, tool calls and observations to complete tasks. (stub, low) · ai
- [[loss-functions]] — A number measuring how wrong a model's predictions are; training minimises it. (stub, low) · ai
- [[low-rank-adaptation-lora]] — Adapting a model by training small low-rank update matrices instead of all its weights. (stub, low) · ai
- [[mechanistic-interpretability]] — Reverse-engineering what the internal components of a neural network compute. (stub, low) · ai
- [[mixture-of-experts]] — Routing each token to a few specialist sub-networks so capacity grows without proportional compute. (stub, low) · ai
- [[neural-networks]] — Layered functions of weighted sums and non-linearities, trained to fit data. (stub, low) · ai
- [[overfitting-and-generalization]] — A model fitting its training data so closely that it fails on new data. (stub, low) · ai
- [[positional-encoding]] — Injecting token order into a model that otherwise treats its input as an unordered set. (stub, low) · ai
- [[probability-and-statistics-basics]] — Describing uncertainty with distributions, expectation, conditional probability and Bayes' rule. (stub, low) · science
- [[prompt-engineering]] — Designing model inputs, including instructions and examples, to steer outputs. (stub, low) · ai
- [[prompt-injection]] — Untrusted text in a model's context hijacking its instructions. (stub, low) · ai
- [[quantization]] — Storing weights in fewer bits to cut memory use and speed up inference. (stub, low) · ai
- [[regularization]] — Techniques that constrain a model to reduce overfitting, such as weight decay and dropout. (stub, low) · ai
- [[reinforcement-learning-basics]] — Learning to act by maximising cumulative reward through interaction with an environment. (stub, low) · ai
- [[reinforcement-learning-from-human-feedback]] — Using human preference judgments to train a reward signal and tune model behaviour. (stub, low) · ai
- [[retrieval-augmented-generation]] — Fetching relevant documents at query time and giving them to a model as context. (stub, low) · ai
- [[scaling-laws]] — Empirical relationships between model size, data, compute and loss. (stub, low) · ai
- [[self-attention]] — A mechanism letting each position in a sequence weigh information from all other positions. (stub, low) · ai
- [[supervised-fine-tuning]] — Continuing training on curated examples to specialise or instruction-tune a pretrained model. (stub, low) · ai
- [[supervised-learning]] — Learning a mapping from inputs to labels using examples. (stub, low) · ai
- [[tokenization]] — Splitting text into sub-word units that a language model reads and predicts. (stub, low) · ai
- [[tool-use-and-function-calling]] — A model emitting structured calls to external functions and using their results. (stub, low) · ai
- [[train-validation-and-test-splits]] — Holding out data to estimate how a model performs on examples it has not seen. (stub, low) · ai
- [[transformer-architecture]] — Stacked blocks of attention and feed-forward layers with residual connections; the basis of modern language models. (stub, low) · ai
- [[vector-search]] — Finding items whose embeddings are nearest to a query embedding. (stub, low) · ai

## Open questions

- [[can-hallucination-be-eliminated-or-only-reduced]] — Whether any training or retrieval approach can bring fabricated statements to zero, or only lower their rate. (stub, low) · ai
- [[do-language-models-build-internal-world-models]] — Whether next-token prediction leads models to represent the underlying structure of the world, or mainly surface statistics. (stub, low) · ai
- [[do-scaling-laws-keep-holding-as-models-and-data-grow]] — Whether the empirical loss-versus-compute trends continue, and whether lower loss keeps translating into useful capability. (stub, low) · ai
- [[how-reliable-is-llm-as-a-judge-evaluation]] — When model-based graders agree with human judgment, and where they are biased. (stub, low) · ai
