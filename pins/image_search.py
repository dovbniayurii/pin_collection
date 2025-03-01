from pinecone import Pinecone
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import requests
from io import BytesIO
import base64

# Initialize Pinecone
#pc = Pinecone(api_key="pcsk_6pkmwU_5WC2wWq5j4KGq8S1QgLGnGkByZroAcSHRKLDh2YnjgfssPqomenV6ZkAPv7SaxM")
#index_name = "pin-collection-image-prod"
#index = pc.Index('index_name')
index = []
# Initialize CLIP model for embedding generation
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Function to generate embedding for the test image
def generate_embedding(image_path_or_url):
    try:
        # Load image from URL or local file
        if image_path_or_url:
            #response = requests.get(image_path_or_url)
            image = Image.open(BytesIO(image_path_or_url)).convert("RGB")
        else:
            image = Image.open(image_path_or_url).convert("RGB")

        # Generate embedding
        inputs = processor(images=image, return_tensors="pt", size=224)
        outputs = model.get_image_features(**inputs)
        return outputs[0].detach().numpy().tolist()  # Convert to list for querying
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None


def generate_embedding_from_base64(image_base64):
    try:
        # Decode base64 to image
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data)).convert("RGB")

        # Generate embedding
        inputs = processor(images=image, return_tensors="pt", size=224)
        outputs = model.get_image_features(**inputs)
        return outputs[0].detach().numpy().tolist()  # Convert to list for querying
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
    
# Test image input (replace with your image URL or local path)
test_image_url = "https://pinandpop.s3.amazonaws.com/images/pinails/91083_TUGm_pinail.jpg"

# Generate embedding for the test image
test_embedding = generate_embedding(test_image_url) # use this function: generate_embedding_from_base64(base64 image) if you want to use base64 image.


if test_embedding:
    # Perform similarity search in Pinecone
    search_results = index.query(vector=test_embedding, top_k=5, include_metadata=True)

    # Display the results
    for match in search_results["matches"]:
        print(f"ID: {match['id']}, Score: {match['score']}")
        print(f"Metadata: {match['metadata']}")
else:
    print("Failed to generate embedding for the test image.")
