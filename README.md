# Nebius_AI_performance

Useful links:
- LearnPyTorch: https://github.com/mohameddhameem/NLPWithPyTorch/tree/master
- Serverless colaboration: https://github.com/mnrozhkov/serverless-cookbook?tab=readme-ov-file

## 02_LLM_architecture:
- a nice website with the LLM leaderboard on benchmark datasets - https://llm-stats.com/
- 

## Useful tools and tricks:
to reduce the size of the video files run the following command:
```
ffmpeg -i Week1_01_agents_lesson_01_20260317_Recording_1920x1080.mp4 \
-vf "fps=2,scale='trunc(iw*0.8/2)*2:-2'" \
-c:v libx265 -crf 28 -preset fast -tune animation \
-ac 1 -c:a aac -b:a 64k \
-tag:v hvc1 -movflags +faststart \
Week1_01_agents_lesson_01_20260317_Recording_1920x1080.2fps.mp4
```
