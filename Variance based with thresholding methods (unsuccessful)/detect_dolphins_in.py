import cv2
import pandas as pd
import os
from tqdm import tqdm
import numpy as np

# def initialize_video_capture(video_path):
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         raise IOError(f"Failed to read the video: {video_path}")
#     return cap

# def get_video_properties(cap):
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     return fps, frame_width, frame_height, total_frames

# def create_video_writer(output_dir, segment_index, fourcc, fps, frame_dimensions):
#     output_path = os.path.join(output_dir, f"segment_{segment_index}.mp4")
#     return cv2.VideoWriter(output_path, fourcc, fps, frame_dimensions), output_path

# def split_frame_into_quadrants(frame, frame_width, frame_height):
#     return [
#         frame[0:frame_height, 0:frame_width],  # upper left
#         frame[0:frame_height, frame_width:2*frame_width],  # upper right
#         frame[frame_height:2*frame_height, 0:frame_width],  # lower left
#         frame[frame_height:2*frame_height, frame_width:2*frame_width]  # lower right
#     ]

# def update_motion_status(motion_detected, motion_frame_count, fps, frame_count, motion_times):
#     if not motion_detected:
#         motion_detected = True
#         motion_times.append(frame_count / fps)  # Start time
#     motion_frame_count += 1
#     return motion_detected, motion_frame_count

# def finalize_motion_segment(motion_detected, video_writer, frame_count, fps, motion_times, rows_list, current_output_path):
#     if motion_detected and video_writer is not None:
#         video_writer.release()
#         motion_times.append(frame_count / fps)  # End time
#         rows_list.append({"Segment": len(rows_list) + 1, "Start": motion_times[-2], "End": motion_times[-1], "File": current_output_path})
#     return False, 0, None

# def calculate_mean_frame(video_path):
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print(f"Failed to read the video: {video_path}")
#         return None

#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     sum_frame = None

#     for _ in tqdm(range(total_frames), desc="Calculating mean frame"):
#         ret, frame = cap.read()
#         if not ret:
#             break
#         if sum_frame is None:
#             sum_frame = np.float32(frame)
#         else:
#             cv2.accumulate(frame, sum_frame)

#     mean_frame = sum_frame / total_frames
#     cap.release()

#     return mean_frame

# def find_dolphins_in(video_path, duration_threshold=3.0, contour_threshold=10, skip_frames=2):
#     cap = initialize_video_capture(video_path)
#     fps, frame_width, frame_height, total_frames = get_video_properties(cap)

#     output_dir = os.path.join(os.path.dirname(video_path), "detected_dolphins")
#     os.makedirs(output_dir, exist_ok=True)
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')

#     motion_times, rows_list = [], []
#     frame_count, motion_frame_count = 0, 0
#     video_writer, current_output_path = None, ""
#     motion_detected = False

#     average_frames = [None] * 4  # Initialize background for each sub-frame

#     with tqdm(total=total_frames // skip_frames, desc=f"Processing Video {video_path}") as pbar:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             if frame_count % skip_frames != 0:
#                 frame_count += 1
#                 continue

#             frames = split_frame_into_quadrants(frame, frame_width, frame_height)
#             motion_detected_in_frame = False
#             for i, sub_frame in enumerate(frames):
#                 if frame_count == 0:
#                     average_frames[i] = np.float32(sub_frame)
#                 else:
#                     motion_detected_in_frame |= detect_motion(sub_frame, average_frames[i], contour_threshold)
#                     cv2.accumulateWeighted(sub_frame, average_frames[i], 0.01)

#             if motion_detected_in_frame:
#                 motion_detected, motion_frame_count = update_motion_status(motion_detected, motion_frame_count, fps, frame_count, motion_times)
#                 if motion_frame_count >= duration_threshold * fps:
#                     if video_writer is None:
#                         video_writer, current_output_path = create_video_writer(output_dir, len(rows_list) + 1, fourcc, fps, (frame_width*2, frame_height*2))
#                     video_writer.write(frame)
#             else:
#                 motion_detected, motion_frame_count, video_writer = finalize_motion_segment(motion_detected, video_writer, frame_count, fps, motion_times, rows_list, current_output_path)

#             frame_count += 1
#             pbar.update(1)

#     if video_writer is not None:
#         video_writer.release()
#     cap.release()
#     return pd.DataFrame(rows_list)


# def detect_motion(sub_frame, average_frame, contour_threshold):
#     background = cv2.convertScaleAbs(average_frame)
#     diff_frame = cv2.absdiff(sub_frame, background)
#     gray = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale if not already
#     _, thresh_frame = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
#     thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

#     cnts, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     motion_detected = any(cv2.contourArea(contour) >= contour_threshold for contour in cnts)

#     return motion_detected



# video_path = "/home/alexis/Desktop/testvideo_2min.mp4"
# motion_df = find_dolphins_in(video_path)
# print(motion_df.head())


# Idée non aboutie : regarder la moyenne et la variance de mes 4 sous images, modifier le binary threshold en fonction de la vraianxce de la frame en utilisant un erelation linéaire


def initialize_video_capture(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Failed to read the video: {video_path}")
    return cap

def get_video_properties(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return fps, frame_width, frame_height, total_frames

def create_video_writer(output_dir, segment_index, fourcc, fps, frame_dimensions):
    output_path = os.path.join(output_dir, f"segment_{segment_index}.mp4")
    return cv2.VideoWriter(output_path, fourcc, fps, frame_dimensions), output_path

def split_frame_into_quadrants(frame, frame_width, frame_height):
    return [
        frame[0:frame_height, 0:frame_width],  # upper left
        frame[0:frame_height, frame_width:2*frame_width],  # upper right
        frame[frame_height:2*frame_height, 0:frame_width],  # lower left
        frame[frame_height:2*frame_height, frame_width:2*frame_width]  # lower right
    ]

def update_motion_status(motion_detected, motion_frame_count, fps, frame_count, motion_times):
    if not motion_detected:
        motion_detected = True
        motion_times.append(frame_count / fps)  # Start time
    motion_frame_count += 1
    return motion_detected, motion_frame_count

# def finalize_motion_segment(motion_detected, video_writer, frame_count, fps, motion_times, rows_list, current_output_path):
#     if motion_detected and video_writer is not None:
#         video_writer.release()
#         motion_times.append(frame_count / fps)  # End time
#         video_writer.release()
#         if len(motion_times) >= 2 and (motion_times[-1] - motion_times[-2]) >= 2.0:
#             rows_list.append({"Segment": len(rows_list) + 1, "Start": motion_times[-2], "End": motion_times[-1], "File": current_output_path})
#         video_writer = None

#     cap.release()

def calculate_subframe_variances(video_path, skip_frames=3):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to read the video: {video_path}")
        return None

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize sums and sum of squares
    sum_frames = [np.zeros((frame_height, frame_width, 3), np.float64) for _ in range(4)]
    sum_squares = [np.zeros((frame_height, frame_width, 3), np.float64) for _ in range(4)]
    frame_count = 0

    for _ in tqdm(range(total_frames // skip_frames), desc="Calculating variances"):
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % skip_frames != 0:
            frame_count += 1
            continue

        # Split frame into 4 parts and accumulate
        subframes = [frame[0:frame_height, 0:frame_width], frame[0:frame_height, frame_width:2*frame_width],
                     frame[frame_height:2*frame_height, 0:frame_width], frame[frame_height:2*frame_height, frame_width:2*frame_width]]

        for i, sf in enumerate(subframes):
            sum_frames[i] += sf
            sum_squares[i] += sf.astype(np.float64) ** 2

        frame_count += 1

    # Calculate variance for each subframe
    variances = []
    N = frame_count
    for sum_frame, sum_square in zip(sum_frames, sum_squares):
        mean = sum_frame / N
        
        variance = (sum_square / N) - (mean ** 2)
        variances.append(variance)
    means = [sum_frame / N for sum_frame in sum_frames]

    cap.release()
    mean_image = np.uint8(means[0])
    cv2.imshow("Mean Image", mean_image)
    cv2.imshow("Mean Image", np.uint8(means[1]))
    cv2.imshow("Mean Image", np.uint8(means[2]))  # Affiche l'image moyenne
    cv2.waitKey(0)  # Attend qu'une touche soit pressée
    cv2.destroyAllWindows()  # Ferme toutes les fenêtres OpenCV

    return means, variances

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)  # Apply Gaussian blur
    return blurred

def find_dolphins_in(video_path, duration_threshold=1.0, contour_threshold=1000, skip_frames=5):
    cap = initialize_video_capture(video_path)
    fps, frame_width, frame_height, total_frames = get_video_properties(cap)

    output_dir = os.path.join(os.path.dirname(video_path), "detected_dolphins")
    os.makedirs(output_dir, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    motion_times, rows_list = [], []
    frame_count, motion_frame_count = 0, 0
    video_writer, current_output_path = None, ""
    motion_detected = False
    ret, frame = cap.read()
    background_frame = frame
    background_frame = process_frame(background_frame)
    with tqdm(total=total_frames // skip_frames, desc=f"Processing Video {video_path}") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % skip_frames != 0:
                frame_count += 1
                continue
            # print(frame.shape, background_frame.shape)
            frame_pro = process_frame(frame)
            # print(frame.shape, background_frame.shape)
            motion_detected_in_frame = False
            if detect_motion(frame_pro, background_frame, contour_threshold, frame_height, frame_width):
                motion_detected_in_frame = True
                cv2.accumulateWeighted(frame_pro.astype(np.float32), background_frame.astype(np.float32), 0.01)

            if motion_detected_in_frame:
                if not motion_detected:
                    motion_detected = True
                    motion_times.append(frame_count / fps)  # Start time
                    current_output_path = os.path.join(output_dir, f"segment_{len(rows_list) + 1}.mp4")
                    video_writer = cv2.VideoWriter(current_output_path, fourcc, fps, (frame_width, frame_height))
                if video_writer is not None:
                    video_writer.write(frame)
            elif motion_detected:
                motion_detected = False
                motion_times.append(frame_count / fps)  # End time
                video_writer.release()
                video_writer = None
                if (motion_times[-1] - motion_times[-2]) >= duration_threshold:
                    rows_list.append({"Segment": len(rows_list) + 1, "Start": motion_times[-2], "End": motion_times[-1], "File": current_output_path})

            frame_count += 1
            pbar.update(1)

    if video_writer is not None:
        video_writer.release()
        motion_times.append(frame_count / fps)  # End time
        if (motion_times[-1] - motion_times[-2]) > duration_threshold:
            rows_list.append({"Segment": len(rows_list) + 1, "Start": motion_times[-2], "End": motion_times[-1], "File": current_output_path})
        video_writer = None

    cap.release()
    return pd.DataFrame(rows_list)

def detect_motion(sub_frame, background, contour_threshold, frame_height, frame_width):
    motions_detected = []
    diff_frame = cv2.absdiff(sub_frame, background)
    _, thresh_frame = cv2.threshold(diff_frame, 3, 255, cv2.THRESH_BINARY)
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
    thresh_frames = split_frame_into_quadrants(thresh_frame, frame_height=frame_height, frame_width=frame_width)
    for thresh in thresh_frames:

        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = any(cv2.contourArea(contour) >= contour_threshold for contour in cnts)
        motions_detected.append(motion_detected)
    return any(motions_detected)



video_path = "/home/alexis/Desktop/testvideo_2min.mp4"
motion_df = find_dolphins_in(video_path)
print(motion_df.head())
# mf = calculate_subframe_variances(video_path=video_path)

def analyze_videos_in_folder(folder_path):
    global_df = pd.DataFrame()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.mp4'):
                video_path = os.path.join(root, file)

                try:
                    motion_df = find_dolphins_in(video_path)
                    if not motion_df.empty:
                        # Create a CSV file in the same directory as the video, with a similar name
                        csv_file_name = file.rsplit('.', 1)[0] + '_analyzed.csv'
                        csv_file_path = os.path.join(root, csv_file_name)
                        motion_df.to_csv(csv_file_path, index=False)
                        print(f"Data saved to {csv_file_path}")

                    motion_df['video_name'] = file
                    global_df = pd.concat([global_df, motion_df], ignore_index=True)
                except Exception as e:
                    print(f"Error processing file {video_path}: {e}")

    # Save the global DataFrame as a CSV file in the main folder
    global_csv_path = os.path.join(folder_path, 'analyzed_videos_global_data.csv')
    global_df.to_csv(global_csv_path, index=False)
    print(f"Global data saved to {global_csv_path}")

    return global_df

# if motion:
#                 if video_writer is None:
#                     motion_times.append(frame_count / fps)  # Start time
#                     current_output_path = os.path.join(output_dir, f"segment_{len(rows_list) + 1}.mp4")
#                     video_writer = cv2.VideoWriter(current_output_path, fourcc, fps, (frame_width, frame_height))

#                 video_writer.write(frame)
#             elif video_writer is not None:
#                 video_writer.release()
#                 video_writer = None
#                 motion_times.append(frame_count / fps)  # End time
#                 if (motion_times[-1] - motion_times[-2]) > duration_threshold:
#                     rows_list.append({"Segment": len(rows_list) + 1, "Start": motion_times[-2], "End": motion_times[-1], "File": current_output_path})