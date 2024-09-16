# Story Book Editor Version 0.0.1

Story Book Editor is a tool for creative writers to create stories, audiobooks, visual novels, translations, and transform their stories to other formats.

This project is currently in alpha state and actively looking for alpha testers willing to try the tools. Check the presentation video:

[Watch the presentation video](https://youtu.be/tVKh1-1ham4)

## SECTIONS

- **[PRESENTATION](#presentation)**: Project presentation.
- **[BACK-END SERVICES INSTALLATION INSTRUCTIONS](#back-end-services-installation-instructions)**: Instructions to get the backend up and running.
- **[FRONT-END INSTALLATION INSTRUCTIONS](#front-end-installation-instructions)**: Instructions to get the frontend up and running.
- **[SESSIONS](#sessions)**: Recorded sessions where we use the tool to create.

## FOLDERS

- **[AI](/AI)**: All the back-end source code to run AI services.
- **[Backend](/Backend)**: All the source code and SQL database structure to locally store the projects.
- **[Stories](/Stories)**: Public domain example stories ready for the tool.

## PRESENTATION

This tool consists of four key modules:

- **Audiobook Creation Helper**
- **Creative Writing Helper**
- **Translation Helper**
- **Format Adaptation Helper**

### 1. Audiobook Creation

The audiobook creation module helps you turn your story into an engaging audiobook. Here’s how it works:

- First, the system summarizes your story and identifies all the characters involved.
- Next, you can assign distinct voices to each character.
- Then, the system analyzes the text, determining which character speaks in each dialogue or paragraph.
- You can also enhance the experience by adding images, sound effects, and music.

Once all this information is set, simply press a button to generate your audiobook.

### 2. Creative Writing

We support you throughout the entire drafting process. Here’s what we offer:

- First, we help you define characters, locations, and plot elements.
- Using this information, the system outlines key events for each chapter.
- For each chapter, we guide you in drafting its content.

In the end, it’s up to you to orchestrate these elements and create your magical story.

### 3. Translation

Our translation module supports multi-language story creation. Here’s how it works:

- First, we make a copy of a story previously introduced in the system.
- Next, select the target language of your translation.
- The system will guide during the process.

### 4. Format Adaptation

This tool allows you to transform your story into other formats. For instance:

- Visual novels
- Comics
- Audiobooks
- Screenplays

With this flexibility, your story can reach various audiences in different formats.

### 5. Looking for testers

We are launching a beta test and seeking feedback from creative individuals interested in shaping the tool's future. 

Head over to our GitHub page, and follow the instructions to install the back-end services, which allow you to generate images, audio effects, and music locally for free. 

Once the services are up and running, contact us at [alpha.tester@infinitemonkeymachine.com](mailto:alpha.tester@infinitemonkeymachine.com), for access to the tool. After everything is set up, you’ll be able to create freely and help us determine the next steps.

## BACK-END SERVICES INSTALLATION INSTRUCTIONS

In the next video it's explained the process step-by-step about how to set up your back-end:

[Backend Setup Presentation](https://youtu.be/alOxMe5vhKE)

Here are all the steps:

### 1. Hardware Setup

Ideally, you should have a dedicated machine with a GPU that has CUDA enabled. Only with this hardware will you be able to get results in reasonable times. You can still run everything on the same machine, but it is ideal to have two machines. In my setup, I have a Jetson Orin as a dedicated machine for all AI operations while working on another machine.

### 2. Software Setup

You should be comfortable to perform some basic programming related operations. You will need to install all the necessary Python libraries in order to make it work. If you have previously installed any repository of an AI tool you should be good to go. There are plenty of good tutorials out there about help installing Python libraries or even you can ask any LLM about how to install that libraries.

### 3. Setting Up the LLM Provider

The system works so far with Open AI, Mistral and Google Large Language Models. You will need to create developer accounts with the providers in order to have the keys that will allow you to access to their services.

Once with the keys you need to open this file and set the values with the right access keys:
```
os.environ["OPENAI_API_KEY"] = 'USER_YOUR_OWN_OPEN_AI_API_KEY'
os.environ["MISTRAL_API_KEY"] = 'USER_YOUR_OWN_MISTRAL_AI_API_KEY'
os.environ["GOOGLE_API_KEY"] = 'USER_YOUR_OWN_GOOGLE_AI_API_KEY'
```

### 4. Setting Up the Image Provider

Just in case that you are not deploying Flux locally and OpenAI Dall.e 2 and 3 models are not enough for you, you have the option to set up 1 more providers for image generation:

- **1. Stability**
```
self.stability_config = 'USER_YOUR_OWN_STABILITY_AI_API_KEY'
```
- **2. Scenario:** If you want to use the character portrait generation you will have to create an account with Scenario provider and copy it here:
```
self.scenario_config = 'USER_YOUR_OWN_SCENARIO_AI_API_KEY'
```

### 5. The most basic set up: LLM Providers

Now you need to run the services you are going to use. 

For example, if you want to use OpenAI ChatGPT-4-Omni-Mini. Run:
```
$ python OpenAIEnglishServer.py
```

This service will be listening in the port 5000. If you want to run any other provider just open to file to know in what port the service is listening.

In order to test it, we are going to need to download [Download Postman](https://www.postman.com/downloads/), a software that allows to test service endpoints. 

- 1. Once installed create a new call
- 2. Select POST mode
- 3. Type the address where your service is located http://XXX.XXX.XXX.XXX:5000/ai/question (Where XXX.XXX.XXX.XXX is the local IP of that machine, for example 192.168.0.246)
- 4. Go to the tab "Body" and then to "raw" and paste this:
```
{
	"userid": 10,
	"username": "not-used",
	"password": "not-used",
	"conversationid": "Any_Word_To_Keep_Track",
	"question": "What can you tell me in less than 100 words about the city of Barcelona?",
	"chain": true,
	"debug": true
}
```	
- 5. Press "Send" button.
	
Since the option "chain" is true, this is a conversation and it will remember,  so you can do a follow up question by asking another thing like this:
```	
{
	"userid": 10,
	"username": "not-used",
	"password": "not-used",
	"conversationid": "Any_Word_To_Keep_Track",
	"question": "What do you recommend me to visit there?",
	"chain": true,
	"debug": true
}
```	
Since it works with memory it will remember that you asked about Barcelona and it will take it from there.

You can test the same process for all the providers and configurations in order to test that everything is up an running. 
Don't forget to change the port number.

### 6. Speech Generation

We need to install the XTTS solution in order for the system to generate the speeches. 
So go to their repository page [Coqui-ai TTS](https://github.com/coqui-ai/TTS) and follow their instructions to install the local service.

Once finished the installation we need to create a sound of silence in order for our script to work. 
So in the same folder where you are going to run the script, type:
```	
$ ffmpeg -f lavfi -i anullsrc=r=11025:cl=mono -t 0.5 silence.wav
```	
Now you are going to start the next process in a different terminal:
```
$ python ServerSpeechGeneration.py
```

Back to **Postman**, we first need to upload a voice track for the system to use it in the speech generation:

- 1. Create a new call
- 2. Select POST mode
- 3. Type the address where your service is located http://XXX.XXX.XXX.XXX:6000/ai/speech/voice
- 4. Go to the tab "Body" and then to "form-data" and fill the parameters:
```	
"project": "My First Test",
"username": "not-used",
"voice": "VoiceTrack",
"language": "en"
"file": select the voice track you want to use.
```			
- 5. Press "Send" button to upload the track.

Now that we have uploaded the voice track, we can proceed to use it to synthesize speech.

- 1. Create a new call
- 2. Select POST mode
- 3. Type the address where your service is located http://XXX.XXX.XXX.XXX:6000/ai/speech
- 4. Go to the tab "Body" and then to "raw" and paste this:
```		
{
	"project": "My First Test",
	"username": "not-used",
	"password": "not-used",
	"voice": "VoiceTrack",
	"speech": "This is the text that I want you to speech",
	"language": "en",
	"emotion": "Happy",
	"speed": 1
}
```			
- 5. Press "Send" button.
	
Now, if everything has worked, you can save the result in and OGG file and you can play it. 

If you use CUDA a text of this size can take around 10 seconds. If you are not using CUDA you can multiple by 5 the time it takes to generate.

### 7. Image Generation

It's strongly recommended that you use Flux as a local free image generator. The open source branch of Stable Diffusion doesn't offer an acceptable quality and paid options are extraordinary expensive considering that during the creation of the audiobooks maybe you could have asked around 150 images for a 200 pages story. Flux with Schnell data is the best option for comercial purposes.

To install Flux and work with schnell data go to their website and follow their instructions:

[Black Forest Lab's Flux Github](https://github.com/black-forest-labs/flux)

Once everything has been installed you should modify the file **demo_gr.py** in order for the service to be enabled to all the computers in the local network:

Replace the last line:
```			
$ demo.launch(share=args.share)
```			

with:
```	
$ demo.launch(share=args.share, server_name="0.0.0.0", server_port=7869)
```	

Now you can run:
```	
$ python3 demo_gr.py --name flux-schnell --device cuda --share
```	

There is a front-end you can use, but we are going to see how it's integrated with our project. 

Now that we have our service running we can test it. Go back to **Postman**:

- 1. Create a new call
- 2. Select POST mode
- 3. Type the address where your service is located http://XXX.XXX.XXX.XXX:5000/ai/image (It's the port 5000, make sure the script "OpenAIEnglishServer.py" is running)
- 4. Go to the tab "Body" and then to "raw" and paste this:
```		
{
	"userid": -1,
	"username": "not-used",
	"password": "not-used",
	"description": "A beautiful rainbow in a happy world",
	"provider": 0,
	"exclude": "",
	"steps": 10,
	"width": 512,
	"height": 512
}
```			
- 5. Press "Send" button.

If everything goes as expected you should be able to save the result into a PNG file and open it. 
If you are using CUDA the image generation process should take around 30 seconds.

### 8. Audio and Music Generation

During the analysis of the text we can extract information in order to find out what sound effects or melodies we can play during the narration. In order to generate this sounds we are going with AudioCraft. So you need to follow the instructions in their repository:

[Meta's Audiocraft Github](https://github.com/facebookresearch/audiocraft)

So once you have started their service. We should run our code:
```
$ python3 ServerAudioGeneration.py
```

Now that we have our service running we can test it. Go back to Postman:

Creating music:

- 1. Create a new call
- 2. Select POST mode
- 3. Type the address where your service is located http://XXX.XXX.XXX.XXX:5000/ai/music
- 4. Go to the tab "Body" and then to "raw" and paste this to create a melody:
```	
{
	"userid": -1,
	"username": "not-used",
	"password": "not-used",		
	"description": "a flute playing classical music",
	"duration": 8
}
```		
- 5. Press "Send" button.

Now, if everything has worked, you can save the result in and OGG file and you can play it. 

### 9. Local Database

In order to store all the data, you are going to create, we are going to create a local webserver with XAMPP. Go to their website follow the instructions:

[Apache Friends XAMPP webserver](https://www.apachefriends.org/download.html)

Once you got it up and running we need to make some changes for our project to work:

- 1. For the file **httpd.conf**: 
```		
Listen 80 -> Listen 8080
```	
- 2. For the file **PHP.ini**
```	
max_execution_time = 1800
max_input_time = 1800
memory_limit = 2048M
upload_max_filesize = 2048M
post_max_size = 2048M
```	
- 3. For the file **my.ini**
```	
max_allowed_packet=1024M
```	
- 4. Now you can go to the **PHPMyAdmin** and create the database: **aibookeditor -> utf8_general_ci**
- 5. Next, you can **import** the basic database structure.
- 6. Finally we need to create the folder where there will be our **scripts that will work as endpoints** to store the data in that database: **xammp\htdocs\aibookeditor**
- 7. Finally you will have to open the file and replace the global variable: **xammp\htdocs\aibookeditor\ConfigurationUserManagement.php**
```	
$SPEECH_UPLOAD_ADDRESS = "http://XXX.XXX.XXX.XXX:5000/ai/speech/voice"; // (Where XXX.XXX.XXX.XXX is the local IP of that machine, for example 192.168.0.246)
```	

### 10. Backend Services Conclusion

You don't need to have all the services up and running for the system to work. It will depend on your needs.

For example:

- 1. **For Text analysis and creation:**

    If you only want to extract information about your text or use the tool to generate a story. In this case you only need up to (THE MOST BASIC SET UP (TESTING ONLY LLM PROVIDERS))
	
- 2. **For Pure audiobooks.**

	If you only want to create audiobooks, no sound effects, no music, no images. Then you need up to (4-SPEECH GENERATION)
	
- 3. **For Visual Novels, without sounds.**

	If you want to add images, but no sounds effects or melodies. The you need up to (5-IMAGE GENERATION)

Of course, in all the cases you will also need to install the database to store the data.

Now you can contact us, at [alpha.tester@infinitemonkeymachine.com](mailto:alpha.tester@infinitemonkeymachine.com), to request the front-end software, we will create an account so you have access.

## FRONT-END INSTALLATION INSTRUCTIONS

After setting up the server and contacting us to get access, you can download the software and run it.

Check the video: [Frontend Setup Video](https://youtu.be/-2tbtXpof7Q)

You can find all the prompts of this session: [Session Prompts](https://www.yourvrexperience.com/apps/aibookeditor/AIBookEditorDisplayPrompts.php?session=The%20Time%20Machine)

Once you have access do the next initial steps:

- 1. Enter your credentials to start using the tool.
- 2. Create a local user: This user will be stored in the local database.
- 3. Set the IP address of the AI endpoints: Go to server settings and set the IP address of the AI services to your machine’s address.

You can now test the system by importing one of the public domain stories that are ready for the system. The book analysis should complete in about 20 minutes. The video shows the entire process, and more extensive sessions are available on our GitHub page.

## SESSIONS

In the following recorded sessions, we demonstrate how to use the tool:

- [Audiobook Creation Session](https://youtu.be/ijXeka1MuBs)
- [Translation Session](https://youtu.be/gThika1ZaOc)
- [Format Adaptation Session](https://youtu.be/tZweJa1ZbUp)
- [Creative Writing Session](https://youtu.be/gBweRa1ZGQx)



