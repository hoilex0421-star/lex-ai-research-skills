# Technical Reading Deck Patterns

Use this reference after `tech-research-deck` triggers and before building slides.

## Research Shapes

### 1. Technology Architecture

Use when the reader first needs the big picture.

Recommended fields:

- Application layer: scenarios and workflows.
- Model layer: foundation models, specialist models, policy/action heads, world models.
- Data layer: internet data, synthetic data, teleoperation data, real deployment data,
  evaluation data.
- AI Infra/runtime: training, inference optimization, simulation, deployment, monitoring.
- Hardware/deployment: cloud, edge, device, sensors, actuators, network.
- Evaluation: benchmark, real-machine test, task success, safety, latency, cost.

Slide output: architecture stack or modular map.

### 2. Technical Route Evolution

Use when the field is moving from an engineering shortcut to higher-ceiling routes.

Narrative:

- Current route: what works today and why it is limited.
- Direction one: route with higher scaling potential.
- Direction two: parallel or alternative route.
- Judgement: which bottleneck shifts from model to data/infra/deployment.

For embodied AI example:

- Current: open-source VLM + DiT/Flow action specialist.
- Direction one: generalist embodied foundation model.
- Direction two: world model as co-trainer/simulator/reward or WAM-style action generator.

Use `$huawei-insight-deck` `dashed_panel`, `route_node`, and `arrow` for the three-panel route map.

### 3. Route Comparison

Use a table only when the audience must compare dimensions precisely.

Good dimensions:

- scalability;
- data requirement;
- generalization;
- inference latency/cost;
- engineering maturity;
- deployment constraint;
- representative players.

Keep row labels identical. Put only the differentiating keyword in red.

### 4. Data Flywheel

Use when data quality and deployment loops are becoming the main technical bottleneck.

Recommended argument:

- Lab/demo data is clean and efficient, but lacks real-world noise.
- Real scenario data is noisy and expensive, but contains failures, long-tail cases,
  recovery traces, and business process labels.
- The better company or platform is the one that can collect data more continuously,
  cheaply, structurally, and commercially.

Four judgement dimensions:

- 持续性: stable online task flow.
- 长尾性: failure and corner-case density.
- 结构化: observation/action/result/takeover records become trainable data.
- 商业化: delivery and data collection share the same cost base.

Use `$huawei-insight-deck` `image_case_card` for company examples.

### 5. Trend Judgement

Do not stop at "X is becoming important." State the causal change:

- new data source makes route scalable;
- new model architecture changes the bottleneck;
- evaluation standard exposes prior demo weakness;
- inference optimization makes edge deployment possible;
- real deployment creates a compounding data advantage.

End with implication for the user's domain, for example:

- compute demand shifts from training-only to training + simulation + edge inference;
- model deployment requires low-latency diffusion/flow/world-model inference;
- benchmark/evaluation platforms become ecosystem control points.

## Writing Heuristics

- Use "当前 / 方向一 / 方向二" for route maps.
- Use "本质是..." to translate technical construction into a business-readable sentence.
- Use "代价 / 泛化能力 / 端边侧部署态 / 代表玩家" as judgement anchors.
- Keep slide body copy free of quotation marks unless quoting verbatim, preserving
  an official term, or discussing the wording itself.
- Use `洞察` as the standard label for the top conclusion strip; do not use
  `核心判断`.
- Avoid listing every paper or company. Pick representative cases that clarify route differences.
- Keep claims falsifiable: include date, benchmark, product, or source in notes.

## Page-Level Density

Split the deck if one page needs all three:

- technical mechanism;
- comparison criteria;
- real company evidence.

Preferred split:

1. mechanism/route page;
2. data or deployment evidence page.
