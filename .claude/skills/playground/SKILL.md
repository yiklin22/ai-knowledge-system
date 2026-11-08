---
name: playground
description: Build an interactive concept playground (HTML simulation with sliders and live visuals) for a vault concept, so the user learns by changing variables and watching the result. Use when the user asks to "see", "play with", "visualise" or "simulate" a concept.
---

# Concept playground

1. Run `./kb tutor <concept>` and read the page and its prerequisites. Decide the one idea the playground must make *felt* (e.g. temperature reshaping a token distribution, learning rate making gradient descent diverge, attention weights over a sentence).
2. Write one self-contained file `playgrounds/<slug>.html`: vanilla JS and canvas or SVG, no network, no libraries, works offline, readable in light and dark mode, usable on a phone width.
3. Design for prediction, not watching: a short "predict first" prompt above the controls ("What will happen if you raise the learning rate to 1.5?"), 2 to 4 controls with live output, and a reveal panel explaining the result with a `[[slug]]` reference to the vault page.
4. The mathematics must be correct for the concept. If you simplify (toy dimensions, fake data), say so on the page.
5. Tell the user the path to open. If asked for sharing, offer to publish it with the Artifact tool.
6. Playgrounds are teaching aids, not knowledge: they are not evidence and never cited as sources.
