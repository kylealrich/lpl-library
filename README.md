# LPL Library
This is a GitLab repository for the LPL Library using Amazon Q.

Amazon Q is instructed to do commits only.

## Important
**Don't update the 'Knowledge.txt' file directly.**

Use the 'References' branch/subdirectory for any files (.busclass, .list, .menu, .txt, etc.) you wish Amazon Q to analyze.

Use the 'Inputs' branch/subdirectory for your input data, files, ANA-050, DES-020, etc.

Generated outputs are located in the 'Outputs' branch/subdirectory.

## Prerequisites
1. Git

2. Visual Studio Code

3. Amazon Q Extension

## Cloning the Respository
1. Setup your profile's SSH Keys (skip this part if your profile already has one).

        - Open a terminal with Administrator Rights.

        - Run: ssh-keygen -t ed25519 -C "<comment>".

            -- You may want to use your email address for the comment.

        - Press enter multiple times until a confirmation is displayed, including the information about where your files are stored.

        - Navigate to C:\Users\<user>\.ssh and open the generated '.pub' file using Notepad and copy its content.

        - Go to your Profile's User Settings > SSH Keys > Add new key.

        - Paste the SSH key and click 'Add key'.

2. In the repository page, click the Code then select the option: Open in your IDE - Visual Studio Code (SSH).

3. Select a directory in your local machine, preferably C:\.

4. Wait for the cloning to finish.

## Integrating the LPL Library in your IDE
1. To sync your workspace:

    a. File > Preferences > Settings > Search for 'post commit'.

    b. Change the value of Run a git command after a successful commit to 'Sync'.

2. Open Amazon Q: Chat extension.

3. Chat with Amazon Q with your LPL needs.

## Functionalities
1. Allows Amazon Q to learn, correct itself and store knowledge about Landmark Programming Language (LPL).

2. Guides users with basic to complex syntaxes by asking Amazon Q to give some examples and definitions without the need of using exact prompts.

3. Generates LPL code based on the user's needs.

4. Displays LPL Tips after every response.

5. Automatically commits to the repository.

## How to Teach Amazon Q
Like a human, you can talk to Amazon Q like how you teach a student about something. You can start by asking Amazon Q to analyze a certain LPL syntax and it'll automatically store it to its knowledge base. You may also ask it to generate a simple or complex LPL syntax and if you noticed errors, you can directly correct Amazon Q by saying that the syntax used is incorrect and providing Amazon Q the correct syntax.

As of writing, this integration have a lot of room for improvement. Together, let's strive by correcting Amazon Q and providing it with more examples until the day that this integration can start providing users with accurate guidance with Landmark Programming Language.

## Copyrights
Kyle Alrich Alonzo

Infor

All rights reserved.

*Please don't distribute without consent.*