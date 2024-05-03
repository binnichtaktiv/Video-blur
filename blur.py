import subprocess, os, shutil

filepath = input("File path of the file you want to blur:\n")
fromsec = input("from which second should blurring start? format: 01:02:03 = hh:mm:ss\n")
tosec = input("up to which second should blurring be?\n")
output = input("enter output path:\n")
format = os.path.splitext(filepath)[1]

temp_dir = "temp"
os.makedirs(temp_dir, exist_ok=True)
temp = os.path.abspath(temp_dir)

blur_part = f'ffmpeg -ss {fromsec} -to {tosec} -i "{filepath}" -map 0 -c copy {temp}/blurpart{format}'
subprocess.run(blur_part, shell=True)

blur_video = f'ffmpeg -i {temp}/blurpart{format} -vf "boxblur=50:5" -c:a copy {temp}/blurdvideo{format}'
subprocess.run(blur_video, shell=True)

first_part_normal = f'ffmpeg -ss 0 -to {fromsec} -i "{filepath}" -c copy {temp}/first_part_normal{format}'
subprocess.run(first_part_normal, shell=True)

last_part_normal = f'ffmpeg -ss {tosec} -i "{filepath}" -c copy {temp}/last_part_normal{format}'
subprocess.run(last_part_normal, shell=True)

rewrite_timestamps = f'ffmpeg -i {temp}/first_part_normal{format} -c copy -fflags +genpts -reset_timestamps 1 {temp}/first_part_normal_retimestamped{format}'
subprocess.run(rewrite_timestamps, shell=True)

rewrite_timestamps = f'ffmpeg -i {temp}/last_part_normal{format} -c copy -fflags +genpts -reset_timestamps 1 {temp}/last_part_normal_retimestamped{format}'
subprocess.run(rewrite_timestamps, shell=True)

txt = os.path.join(temp, "input.txt")
with open(txt, 'w') as f:
    f.write(f'file {temp}/first_part_normal_retimestamped{format}\nfile {temp}/blurdvideo{format}\nfile {temp}/last_part_normal_retimestamped{format}')

combine = f"ffmpeg -f concat -safe 0 -i {txt} -c:v copy -c:a copy {output}/censored_video{format}"
subprocess.run(combine, shell=True)

shutil.rmtree(temp)
print("you can find your blurred video here: " + output + "/censored_video" + format)
