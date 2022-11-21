#include "opencv2/opencv.hpp"
#include <iostream>
 
using namespace std;
using namespace cv;

void read_ip_video(string output_video_path)
{
	VideoCapture cap(1); 
	if(!cap.isOpened())
	{
		cout << "Could't read IP video: " << endl;
		return;
	}
	
	int frame_width = cap.get(cv::CAP_PROP_FRAME_WIDTH);
	int frame_height = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
	
	VideoWriter video(output_video_path, cv::VideoWriter::fourcc('M','J','P','G'), 10, Size(frame_width,frame_height));

	Mat frame;
	cap >> frame;

	while (!frame.empty())
	{
		imshow("Video", frame);
		if(waitKey(25) == 27)
			break;

		video.write(frame);
		cap >> frame;
	}
	
	cap.release();
	video.release();

	destroyAllWindows();
}
 
int main()
{
	read_ip_video("ip_video.avi");
}