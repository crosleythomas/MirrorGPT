# Mirror Agent

This directory contains code for the "Mirror Agent" (MA) - the conversational agent that uses stored memory, base language models, fine-tuned language models, and/or other tools to effectively mirror a Subject user.

The Mirror Agent should adapt its responses to the following:
1. Facts - what are the specific details about the Subject that should be factually accurate?
2. Style - *how* does the Subject say things?
3. Setting - does the Subject adapt how they speak (e.g. formal vs informal) or what they share (e.g. share SSN with parents but not with food delivery driver)
4. Voice - the sound of the Subject's voice (for text-to-speech)
5. Look - what does the Subject look like? (for personalized avatars)