<h1 align='center' >github alerts slack bot :robot: </h1>


## What is it? :mag: 
This is a simple bot that serves to send some notifications about GitHub events to Slack channels.

These are the features currently developed:
- notification to inform Pull Requests with conflicts

> Others features may be developed in the future.

<br>

## How it works :factory_worker: 
- GitHub webhook send a request to bot to selected event (Pull Request has been opened, per example)
- It handle the request
  - it check if the request comes from the correct GitHub webhook to avoid fraud
  - it don't send repeated notification with same data on the same day
- Whether yes, the Slack webhook is called to create a message in on channel with the information (a Pull Request is open) 

<br>

## Configuration :gear:
### Create a access token of GitHub
Navigate to **Settings** > **Developer Settings** > **Personal access tokens** > **Generate new token**

The permission `repo` is only need to access necessary datas of yours repositories:
![image](https://user-images.githubusercontent.com/40877357/149664862-d9247ea9-17d3-4f70-8dbc-7b936cd05be7.png)

Save the access token after creating it.

### Create a workflow in Slack
The workflow is the point used to send the notifications and [here there are a tutorial to create one](https://slack.com/help/articles/360035692513-Guide-to-Workflow-Builder).

The only var required in the text is `prs_list`.

You can customize the message of your workflow as you wish:

<div align='center'>
  <img src='https://user-images.githubusercontent.com/40877357/149665467-b376fc4b-c090-49ef-ba81-d0f3546d6fa7.png' alt='example of workflow'>
</div>

After create, save the workflow webhook.

### Deploy the bot
First, create your fork of this project to can perform the deploy.

The our bot is configured to deploy in [Heroku](https://www.heroku.com/). 
Heroku is a cloud platform to deploy your simple projects, they have a free plan that will be enough for us.
You can also choose another cloud platform to do this.

**Create a new app** > **Select the deploy on GitHub** > **Choose your fork of this project**

Greate! If everything is ok, you can see this message:

<div align='center'>
  <img src='https://user-images.githubusercontent.com/40877357/149665992-a61d9617-3c3e-44f4-bbdf-68e3efb011b1.png' alt='success deploy'>
</div>

### Install Redis
[Redis](https://redis.io/) is used to check if one message is send in the past day with the same pull requests.

In the dashboard of your project in Heroku, go to **Resources** > **Find more add-ons**

Select **Redis Enterprise Cloud**. It will probably ask you to set up the credit card on your account, but don't worry, the free plan is enough to our bot.
After set up your credit card, select the free plan and the project of bot to install the Redis.

It is listed in your add-ons if everything is ok:

<div align='center'>
  <img src='https://user-images.githubusercontent.com/40877357/149666456-0bcc557f-825f-4c4f-bf08-2c1680e89fed.png' alt='redis add-on'>
</div>

Access the add-on and complete the Redis url with the datas: `http://rediscloud:password@hostname:port`

Like this:
`http://rediscloud:cofe6kWpNnsdlfkçlç3441kj2l@redis-0000.c11.en-east-1-3.ec2.cloud.redislabs.com:1234`

This will be used to connect our bot with the Redis.

### Create GitHub webhook
**Your repository to track** > **Settings** > **Webhooks** > **add webhook**

In the `Payload URL`, past the URL of your Heroku project and the endpoint `check_conflicts`. Like this: `https://my-heroku-app.herokuapp.com/check_conflicts`

The `Content type` is `application/json`.

I recommend using a [UUID](https://www.uuidgenerator.net/) in the `Secret`. This will ensure the security of the requests. 
Save this secret to use in virtual environments of the project

In the events, select `Let me select individual events.` and select `Pull requests` in the list of events.

Now just save.

### Setting envs
Finally, the last step is set the virtual environments in the Heroku project.

**Heroku project** > **Settings** > **Reveal Config vars**.

Now set this envs:
- SECRET_ACCESS: secret used in GitHub webhook
- ACCESS_TOKEN: your access token of GitHub
- PROJECT_TO_TRACK: project of the GitHub webhook. Example: `jackson541/github-alerts-slack-bot`
- BRANCH_TO_TRACK: the branch of the project that you want to track. Example: `master`
- SLACK_WEBHOOK_LINK: the URL of the workflow created in Slack
- REDIS_URL: the URL created with the datas of Redis. example: `http://rediscloud:cofe6kWpNnsdlfkçlç3441kj2l@redis-0000.c11.en-east-1-3.ec2.cloud.redislabs.com:1234`

You can stop and have your coffee, everything is set up!

<br>

## Contribute :heavy_plus_sign: 
Contribute is always well received! Feel free to open Pull Requests or Issues. :smile: 



