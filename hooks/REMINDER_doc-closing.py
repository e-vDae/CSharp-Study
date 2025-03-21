import os
import sys
import datetime
import webbrowser
import clr
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
from System.Windows import Window, WindowStartupLocation, RoutedEventHandler
from System.Windows.Markup import XamlReader

# Define directory and file path
directory = os.path.join(os.environ["USERPROFILE"], "Documents", "DAE REVIT LOG")
file_path = os.path.join(directory, "DAE_REVIT_LOG.txt")

# Create directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Get current date and time
time_now = datetime.datetime.now()
today_date_str = time_now.strftime("%Y-%m-%d")

# Execute only if the time is past 6 PM
if time_now.hour >= 18:
    # Read the last snooze value and time if the file exists
    Snooze = False
    last_time = None
    last_turn_off_date = None
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in reversed(lines):
                if "Turned off for today" in line:
                    last_turn_off_date = line.split(" | ")[0]
                    break
            
            if lines:
                last_line = lines[-1].strip()
                parts = last_line.split(" | Snooze: ")
                if len(parts) == 2:
                    last_time_str, snooze_value = parts
                    try:
                        last_time = datetime.datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
                        Snooze = snooze_value.strip() == "True"
                    except ValueError:
                        last_time = None
    
    # Check if the last turn off entry is today
    if last_turn_off_date == today_date_str:
        sys.exit()
    
    # If snooze is true, check the time difference
    if Snooze and last_time:
        time_diff = time_now - last_time
        if time_diff.total_seconds() >= 3600:
            Snooze = False  # Change snooze value if time difference is >= 60 minutes
        else:
            sys.exit()

    # Write to file
    log_entry = "{} | Snooze: {}".format(time_now.strftime("%Y-%m-%d %H:%M:%S"), Snooze)
    with open(file_path, "a") as file:
        file.write(log_entry + "\n")

    # Show a window with options if Snooze is False
    if not Snooze:
        xaml = '''
        <Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                Title="Reminder" Height="250" Width="350" Padding="20"
                WindowStyle="None" Background="#3A3B3C"
                WindowStartupLocation="CenterScreen"
                ResizeMode="NoResize">
            <Grid Margin="20">
                <Grid.RowDefinitions>
                    <RowDefinition Height="Auto" />
                    <RowDefinition Height="*" />
                    <RowDefinition Height="Auto" />
                    <RowDefinition Height="Auto" />
                    <RowDefinition Height="Auto" />
                </Grid.RowDefinitions>

                <Button Name="btnClose" Content="X" HorizontalAlignment="Right" Width="30" Height="30" Grid.Row="0" Background="Red" Foreground="White"/>
                <TextBlock Text="Deltek Reminder" HorizontalAlignment="Center" VerticalAlignment="Center" FontSize="24" FontWeight="Bold" Grid.Row="1" Foreground="White"/>
                <Button Name="btnSnooze" Content="Snooze (1hr)" HorizontalAlignment="Center" Width="200" Height="30" Grid.Row="2"/>
                <Button Name="btnOpenDeltek" Content="Open Deltek" HorizontalAlignment="Center" Width="200" Height="30" Grid.Row="3"/>
                <Button Name="btnTurnOff" Content="Turn off for Today" HorizontalAlignment="Center" Width="200" Height="30" Grid.Row="4"/>
            </Grid>
        </Window>
        '''

        window = XamlReader.Parse(xaml)
        window.WindowStartupLocation = WindowStartupLocation.CenterScreen

        def snooze(sender, e):
            with open(file_path, "a") as file:
                file.write("{} | Snooze: True\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            window.Close()

        def open_deltek(sender, e):
            webbrowser.open("https://deltek.dewan-architects.com/")
            window.Close()

        def turn_off(sender, e):
            with open(file_path, "a") as file:
                file.write("{} | Turned off for today\n".format(datetime.datetime.now().strftime("%Y-%m-%d")))
            window.Close()

        def close_window(sender, e):
            window.Close()

        window.FindName("btnSnooze").Click += RoutedEventHandler(snooze)
        window.FindName("btnOpenDeltek").Click += RoutedEventHandler(open_deltek)
        window.FindName("btnTurnOff").Click += RoutedEventHandler(turn_off)
        window.FindName("btnClose").Click += RoutedEventHandler(close_window)

        window.ShowDialog()