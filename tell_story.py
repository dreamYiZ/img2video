from describe_image import process_images
import ollama


def get_story_from_descriptions(descriptions):
    story_parts = [item['description'] for item in descriptions]
    story = " ".join(story_parts)
    return story


def rewrite_story_with_phi4(story):
    res = ollama.chat(
        model="phi4",
        messages=[
            {
                'role': 'user',
                'content': f'Rewrite the following story based on the descriptions: {story}'
            }
        ]
    )
    if 'message' in res and 'content' in res['message']:
        return res['message']['content']
    else:
        return story


def add_story_to_descriptions(descriptions, story):
    words_per_minute = 150  # 假设每分钟朗读150个单词
    story_words = story.split()

    # 计算每个描述应分配的单词数
    num_descriptions = len(descriptions)
    words_per_description = len(story_words) // num_descriptions

    story_parts = []
    current_part = []
    current_word_count = 0
    for word in story_words:
        current_part.append(word)
        current_word_count += 1
        if current_word_count >= words_per_description:
            story_parts.append(" ".join(current_part))
            current_part = []
            current_word_count = 0
    if current_part:
        story_parts.append(" ".join(current_part))

    for idx, description in enumerate(descriptions):
        if idx < len(story_parts):
            description['story_part'] = story_parts[idx]
            description['story_time'] = len(story_parts[idx].split()) / words_per_minute
        else:
            description['story_part'] = ""
            description['story_time'] = 0

    return descriptions


def get_description_and_tell_a_story():
    descriptions = process_images()
    for item in descriptions:
        print(f"Image: {item['filename']}\nDescription: {item['description']}\n")

    story = get_story_from_descriptions(descriptions)
    rewritten_story = rewrite_story_with_phi4(story)
    updated_descriptions = add_story_to_descriptions(descriptions, rewritten_story)

    for item in updated_descriptions:
        print(
            f"Image: {item['filename']}\nDescription: {item['description']}\nStory Part: {item.get('story_part', '')}\nStory Time: {item.get('story_time', 0)}\n")

    return updated_descriptions

def main():
    get_description_and_tell_a_story()


if __name__ == '__main__':
    main()
