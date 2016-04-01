CSV = https://www.license.state.tx.us/DownLoadableContent/Elevator/elevator_data_file.csv

# Source Elevator Data CSV:
# https://www.license.state.tx.us/ElevatorSearch/HelpPage.asp#data
elevator_data_file.csv:
	curl $(CSV) | csvsort > $@


sample_elevator_data_file.csv: elevator_data_file.csv
	head elevator_data_file.csv > sample_elevator_data_file.csv


clean:
	rm -f elevator_data_file.csv


.PHONY: clean
