%read in blf file
canMessageTimetable=blfread("Raw1__20250402232048.blf");
% Exctract time table
canMessageTimetable=canMessageTimetable{1};

%get start and stop time 
startTime=seconds(canMessageTimetable.Time(1));
endTime=seconds(canMessageTimetable.Time(end));

%define sample time 
Ts=0.001;
startTime=round(startTime,3);
endTime=round(endTime,3);

%Convert the messages to a compatible format 

canMessages=canMessageReplayBlockStruct(canMessageTimetable);
save processed.mat canMessages
