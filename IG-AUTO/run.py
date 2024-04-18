import os
from pathlib import Path
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from instagrapi import Client
from datetime import datetime


def get_followers_count(username, password, target_username):
    # Initialize the Instagram client
    client = Client()
    
    # Login to Instagram
    client.login(username, password)
    
    # Get the user object of the target account
    user = client.user_info_by_username(target_username)
    
    # Get the follower count
    followers_count = user.follower_count
    
    # Logout from Instagram
    client.logout()
    
    return followers_count

def post_reel(username, password, video_path, caption):
    # Initialize the Instagram client
    client = Client()
    
    # Login to Instagram
    client.login(username, password)
    
    # Get the current folder path
    current_folder = os.getcwd()
    
    # Concatenate the video filename to the current folder path
    video_folder = os.path.join(current_folder, video_path)
    
    # Upload the reel (video) with caption
    client.clip_upload(video_folder, caption=caption)
    
    # Logout from Instagram
    client.logout()

def calculate_days_left(set_date):
    # Convert the set date string to a datetime object
    set_date_obj = datetime.strptime(set_date, '%Y-%m-%d')
    
    # Get the current date
    current_date = datetime.now()
    
    # Calculate the difference in days between the set date and current date
    delta = set_date_obj - current_date
    
    # Return the number of days left
    return delta.days

def add_text_to_video(input_video, output_video, set_date, followers, font='Calibri', fontsize=50, color='white', bg_color=None, pos=(0, 0)):
    # Calculate the number of days left
    days_left = calculate_days_left(set_date)
    
    # Format followers with comma separators
    comma_followers = "{:,}".format(followers)
    
    # Load the input video clip
    video_clip = VideoFileClip(input_video)
    
    # Create the text string with variables
    text = f"{days_left} days left to prove that the F22\n will gain more followers than\n the Russian ARMY IG Account\n ({comma_followers}/500,000)"
    
    # Create a text clip with the specified text
    text_clip = TextClip(text, fontsize=fontsize, font=font, color=color, bg_color=bg_color)
    
    # Set the duration of the text clip to match the duration of the video clip
    text_clip = text_clip.set_duration(video_clip.duration)
    
    # Set the position of the text clip
    text_clip = text_clip.set_position(pos)
    
    # Composite the video clip and text clip together
    final_clip = CompositeVideoClip([video_clip.set_duration(text_clip.duration), text_clip])
    
    # Add audio from the input video to the final clip
    final_clip = final_clip.set_audio(video_clip.audio)
    
    # Write the final clip to a new video file
    final_clip.write_videofile(output_video, codec='libx264', audio_codec='aac', fps=video_clip.fps)

# IG API:
username = 'username' # Account usernmae
password = 'password' # Account password
target_username = 'targeruser' # Target account for follower retreaval

followers = get_followers_count(username, password, target_username)
print(f"Followers count of {target_username}: {followers}")

#Post Reel
video_path = 'output.mp4'  # Filename is output.mp4 in the current folder
caption = 'Let’s do this! 🦅✈️💸 \n\n #viral #meme #reels #finance #fyp #f22 #usa #usarmy #us'

#Video Info
input_video = 'input.mp4'
output_video = 'output.mp4'
set_date = '2024-06-18'  # Example: Set the date as December 31, 2024

# Customize text properties
font = 'Instagram-Sans'
fontsize = 70
color = 'white'
bg_color = 'none'

# Specify the position in pixels (x, y)
pos = ('center', 250)  # Adjust the coordinates as needed

add_text_to_video(input_video, output_video, set_date, followers, font, fontsize, color, bg_color, pos)
post_reel(username, password, video_path, caption)