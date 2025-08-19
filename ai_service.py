import os
import json
import logging
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_product_content(product_name, affiliate_link, section_name, price=None):
    """
    Generate comprehensive product content using AI
    """
    try:
        # Create a comprehensive prompt for product review generation
        prompt = f"""
        Generate comprehensive marketing content for the product: {product_name}
        Section: {section_name}
        Price: {price if price else 'Not specified'}
        
        Please provide the response in JSON format with the following structure:
        {{
            "short_description": "A brief 2-3 sentence description highlighting key features",
            "full_review": "A detailed product review (300-500 words) covering overview, features, performance, and value proposition",
            "pros": ["List of 4-6 key advantages"],
            "cons": ["List of 2-4 potential drawbacks or limitations"],
            "seo_title": "SEO-optimized title (under 60 characters)",
            "meta_description": "SEO meta description (under 160 characters)"
        }}
        
        Make the content engaging, informative, and helpful for potential buyers. Include specific details about features, build quality, performance, and value for money. The tone should be professional but approachable.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert product reviewer and content writer specializing in affiliate marketing. Create honest, detailed, and engaging product reviews that help consumers make informed decisions."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        content_text = response.choices[0].message.content
        if content_text:
            content = json.loads(content_text)
        else:
            raise Exception("Empty response from AI")
        
        # Add affiliate link call-to-action to the full review
        content["full_review"] += f"\n\n**Ready to purchase?** [Check the latest price and availability here]({affiliate_link}) 🛒"
        
        return content
        
    except Exception as e:
        logging.error(f"Error generating AI content: {str(e)}")
        # Return fallback content if AI fails
        return {
            "short_description": f"Discover the features and benefits of {product_name}. A quality product in the {section_name} category.",
            "full_review": f"# {product_name} Review\n\nThis {product_name} offers excellent value in the {section_name} category. With its combination of quality construction and practical features, it represents a solid choice for consumers.\n\n## Key Features\n- Quality construction and materials\n- User-friendly design\n- Good value for money\n- Reliable performance\n\n## Conclusion\nOverall, the {product_name} delivers on its promises and provides good value for the price point. Whether you're a beginner or experienced user, this product offers the functionality and reliability you need.\n\n**Ready to purchase?** [Check the latest price and availability here]({affiliate_link}) 🛒",
            "pros": ["Quality construction", "Good value for money", "User-friendly design", "Reliable performance"],
            "cons": ["Limited advanced features", "May not suit all use cases"],
            "seo_title": f"{product_name} Review - Is It Worth It?",
            "meta_description": f"Detailed review of {product_name}. Find out about features, pros & cons, and whether it's worth your money."
        }

def generate_section_description(section_name):
    """
    Generate a description for a new section
    """
    try:
        prompt = f"Write a brief, engaging description (2-3 sentences) for a product category called '{section_name}' on an affiliate marketing website. Make it informative and appealing to potential shoppers."
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a marketing copywriter specializing in e-commerce category descriptions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        return content.strip() if content else f"Explore our carefully curated selection of {section_name} products."
        
    except Exception as e:
        logging.error(f"Error generating section description: {str(e)}")
        return f"Explore our carefully curated selection of {section_name} products. Find the best deals and detailed reviews to help you make informed purchasing decisions."
