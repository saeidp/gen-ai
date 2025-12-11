https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html

agent.py
This file is the main agent that you can create and test locally


Docker file
 docker buildx create --use
 docker buildx build --platform linux/arm64 -t my-agent:arm64 --load .

Test locally
docker run --platform linux/arm64 -p 8080:8080 \
  -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
  -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
  -e AWS_SESSION_TOKEN="$AWS_SESSION_TOKEN" \
  -e AWS_REGION="$AWS_REGION" \
  my-agent:arm64

  You can then create ecr repository an ddeploy the image to the ecr
aws ecr create-repository --repository-name my-strands-agent --region us-west-2
docker buildx build --platform linux/arm64 -t account-id.dkr.ecr.us-west-2.amazonaws.com/my-strands-agent:latest --push .
aws ecr describe-images --repository-name my-strands-agent --region us-west-2

Deploy agent runtime
  deploy_agent.py

Invoke agent
  invoke_agent.py

Run invoke_agent.py
  uv run invoke_agent.py