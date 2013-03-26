# Source Elevator Data CSV:
# https://www.license.state.tx.us/ElevatorSearch/HelpPage.asp#data
elevator_data_file.csv:
	wget https://www.license.state.tx.us/DownLoadableContent/Elevator/elevator_data_file.csv

sample_elevator_data_file.csv: elevator_data_file.csv
	head elevator_data_file.csv > sample_elevator_data_file.csv
