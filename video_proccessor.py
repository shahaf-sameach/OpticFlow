import subprocess
import os

class VideoProccessor:

	def __init__(self, file_name):
		self.file_dir = os.path.dirname(os.path.realpath('__file__'))
		self.file_name = os.path.join(self.file_dir, file_name)

	def encode(self, output_file = 'output.mp4' ,fps = 2):
		# ffmpeg_bin = check_output(['which', 'ffmpeg'])
		fps = str(fps)
		output_file = os.path.join(self.file_dir, output_file)
		subprocess.call(['ffmpeg', '-i', self.file_name, '-r', fps, '-y', output_file])
		return output_file
