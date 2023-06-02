import csv
import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self._encrypt_password(password)
        
    def _encrypt_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, password):
        return self.password == self._encrypt_password(password)


class Location:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

class Ride:
    def __init__(self, user, source, destination):
        self.user = user
        self.source = source
        self.destination = destination


class RideSharingSystem:
    def __init__(self, user_file, location_file):
        self.users = self.load_users(user_file)
        self.locations = self.load_locations(location_file)
        self.rides = []
    
    def load_users(self, user_file):
        users = []
        with open(user_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                username = row[0]
                password = row[1]
                user = User(username, password)
                users.append(user)
        return users
    
    def load_locations(self, location_file):
        locations = []
        with open(location_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                name = row[0]
                latitude = float(row[1])
                longitude = float(row[2])
                location = Location(name, latitude, longitude)
                locations.append(location)
        return locations
    
    def save_users(self, user_file):
        with open(user_file, "w", newline="") as file:
            writer = csv.writer(file)
            for user in self.users:
                writer.writerow([user.username, user.password])
    
    def save_locations(self, location_file):
        with open(location_file, "w", newline="") as file:
            writer = csv.writer(file)
            for location in self.locations:
                writer.writerow([location.name, location.latitude, location.longitude])
    
    def register_user(self, username, password):
        user = User(username, password)
        self.users.append(user)
        return user
    
    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.authenticate(password):
                return user
        return None
    
    def add_location(self, name, latitude, longitude):
        location = Location(name, latitude, longitude)
        self.locations.append(location)
    
    def request_ride(self, user, source_name, dest_name):
        source = self.find_location(source_name)
        destination = self.find_location(dest_name)
        if source is None or destination is None:
            return None
        ride = Ride(user, source, destination)
        self.rides.append(ride)
        return ride
    
    def get_user_rides(self, user):
        user_rides = []
        for ride in self.rides:
            if ride.user == user:
                user_rides.append(ride)
        return user_rides

def show_locations():
    locations = ride_sharing_system.load_locations(location_file)
    print(f"Location Name\t\tLatitude\tLongitude")
    for i in locations:
        print(f"{i.name}\t\t{i.latitude}\t\t{i.longitude}")

user_file = "users.csv"
location_file = "locations.csv"
ride_sharing_system = RideSharingSystem(user_file, location_file)

while True:
    print("Welcome To UBER")
    print("What do you want to Choose Today?")
    print("1. Create An Account\n2. Login")
    option = int(input())
    if option == 1:
        name = input("Enter Username : ")
        password = input("Enter a password : ")
        ride_sharing_system.register_user(name, password)
        ride_sharing_system.save_users(user_file)
    elif option == 2:
        name = input("Enter Username : ")
        password = input("Enter password : ")
        logged_in_user = ride_sharing_system.login(name, password)
        if name == 'admin' and password == '123':
            while True:
                print("Welcome ADMIN")
                print("1. Add New Locations\n2. Show All the locations\n3. Show All Users\n4. EXIT")
                option = int(input())
                if option == 1:
                    location_name = input("Enter the first location : ")
                    location_lat = float(input("Enter the latitude"))
                    location_lon = float(input("Enter the latitude"))
                    ride_sharing_system.add_location(location_name, location_lat, location_lon)
                    ride_sharing_system.save_locations(location_file)
                elif option == 2:
                    show_locations()
                elif option == 3:
                    users = ride_sharing_system.load_users(user_file)
                    print("From \t\tTo\t\t")
                    for user in users:
                        logged_in_user = ride_sharing_system.login(user.username, user.password)
                        ride_history = ride_sharing_system.get_user_rides(logged_in_user)
                        for i in ride_history:
                            print(f"{i.source.name}\t\t{i.destination.name}")
                elif option == 4:
                    break
        else:
            if logged_in_user:
                print(f"\nWelcome {logged_in_user.username}")
                
                while True:
                    print("1. Request a Ride\n2. Show All the locations\n3. Show Ride History\n4. EXIT")
                    option = int(input())
                    if option == 1:
                        from_loc = input("Enter the Current location : ")
                        destination = input("Enter the Destination location : ")
                        ride = ride_sharing_system.request_ride(logged_in_user, from_loc, destination)
                        if ride:
                            print("Ride requested successfully!")
                    elif option == 2:
                        show_locations()
                    elif option == 3:
                        ride_history = ride_sharing_system.get_user_rides(logged_in_user)
                        print("From \t\tTo\t\t")
                        for i in ride_history:
                            print(f"{i.source.name}\t{i.destination.name}")
                    elif option == 4:
                        break
            else:
                print("INVALID USERNAME")
