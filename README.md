SPACED REPETITION APP: MOSTLY FOR ME TO BE MORE EFFICIENT WITH LEARNING
(Sections: Description, How to Use, Details, Objects)

>>>Description:

A program that lets you input questions with the answers that you want to learn over time. Every time you answer a question, you answer how well you know it now on scale of 0-3 (0 - you have no idea, 1 - you don't know it, 2 - you know it, 3 - you really know it). Based on your response to the questions, there is a memorization counter that adjusts the time it takes for that question to come up again based on how well you know a question.

-Questions can have tags to associate them with categories

>>>How to Use:

Run the program whenever you want to learn some of the questions, and answer the questions by yourself on paper or a text editor (not on the program), and when you're ready to see the answer, you can view it and submit how well you know the question, and you can move on to the next one.
Interface: Answer Questions, Add Questions, Delete Questions, View Questions -> Edit Questions

-You can view questions from one (or multiple) categories by choosing which tags you want the questions to have
-You can view the questions in a test format so that you don't have to answer each one right away (best way to learn is being tested)
-You can choose to skip a question
-You can delete or add questions

>>>Details:

-memorization counter levels: 1 day | 7 days | 16 days | 35 days | 75 days | 200 days
--then after 200 days, it repeats every 200 days
(Based on Piotr Wozniak's research)
-scale: 0 - moves the memorization counter back one, 1 - keeps counter as is, 2 - moves the counter forward one, 3 - moves the counter forward two
-^ or scale could be a five star scale that the user selects

>>>Objects:

Question:
-variables: memorization counter level, start time, end time, question, answer, tags
-functions: getter/setter (view/change) funcs, increase mem.counter(x), decrease mem.counter(x), delete question
Test:

