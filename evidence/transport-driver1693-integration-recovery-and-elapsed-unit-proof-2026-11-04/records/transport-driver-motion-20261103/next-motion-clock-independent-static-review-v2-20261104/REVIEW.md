# Independent static V2 motion-clock review

No static blocker found. The opt-in `!elapsedFrame || motionFrame` guard resolves the synthetic driver visual priming boundary for production elapsed frames while retaining legacy direct-town behavior. All five source pins and both patch hashes match. V1 acceptance cases are an exact prefix of V2; no original test lines are removed.

The additional actual town/driven-assembly test checks admission, offscreen return and Light restoration with first real frame zero and next frame exact delta. It also protects independent looking while stopped and Continue rebasing travel without pausing the independently active look. The runtime source still advances the qualified driver once per real town frame and horse/wheel phase through accepted swept travel only.

Nothing was applied or executed. Native checks and visible low-FPS acceptance remain required after application; this is not a claim about current PR1693 merge status, natural horse stride, photo quality or world performance.
