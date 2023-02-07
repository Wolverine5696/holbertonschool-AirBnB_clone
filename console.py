#!/usr/bin/python3
"""
Console module that contains the entry point of the command interpreter
"""
import cmd
from models.base_model import *
from models import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    our command interpreter class that will implement
    quit, EOF, help, and a custom prompt (hbnb). An empty line + ENTER
    must not do anything
    """
    prompt = '(hbnb) '
    classes_list = ["BaseModel", "User", "State", "City", "Amenity", "Place",
                    "Review"]
    int_attrs = ["number_rooms", "number_bathrooms", "max_guest",
                 "price_by_night"]
    float_attrs = ["latitude", "longitude"]

    def do_EOF(self, line):
        """Quits console when CTRL + D is pressed"""
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Empty line + ENTER must not execute anything"""
        pass

    def do_create(self, line):
        """
        Creates a new instance of a class and prints the unique id
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split()

        if args[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
            return
        
        new_obj = globals()[args[0]]()
        new_obj.save()
        print(new_obj.id)

    def do_show(self, line):
        """
        Prints the string representation of an instance based on the class name
        and id
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split()

        if args[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_key = args[0] + "." + args[1]
        storage = FileStorage()
        all_objs = storage.all()

        for key, value in all_objs.items():
            if key == obj_key:
                print(value)
                return
        print("** no instance found **")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id,
        saves the change into the JSON file
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split()

        if args[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_key = args[0] + "." + args[1]
        storage = FileStorage()
        all_objs = storage.all()

        for key, value in all_objs.items():
            if key == obj_key:
                del all_objs[key]
                storage.__objects = all_objs
                storage.save()
                return

        print("** no instance found **")

    def do_all(self, line):
        """
        Prints all string representation of all instances based or not on the
        class name
        """
        storage = FileStorage()
        all_objs = storage.all()
        obj_list = []
        check = False

        if not line:
            for key, value in all_objs.items():
                obj_list.append(str(value))
            print(obj_list)
            return

        args = line.split()

        if args[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
            return

        for key, value in all_objs.items():
            if args[0] in key:
                obj_list.append(str(value))
        print(obj_list)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split()

        if args[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_key = args[0] + "." + args[1]
        storage = FileStorage()
        all_objs = storage.all()

        for key, value in all_objs.items():
            if key == obj_key:
                if len(args) < 3:
                    print("** attribute name missing **")
                    return
                if len(args) < 4:
                    print("** value missing **")
                    return
                if args[2] in HBNBCommand.int_attrs:
                    args[3] = int(args[3])
                if args[2] in HBNBCommand.float_attrs:
                    args[3] = float(args[3])
                setattr(value, args[2], args[3])
                storage.save()
                return

        print("** no instance found **")

    def do_count(self, line):
        """
        Retrieve the number of instances of a class
        """
        storage = FileStorage()
        all_objs = storage.all()
        count = 0

        if not line:
            print("** class name missing **")
            return

        args = line.split()

        if args[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
            return

        for key, value in all_objs.items():
            if args[0] in key:
                count += 1
        print(count)

    def precmd(self, line):
        """
        overrides parent method to handle the parsing of commands
        """
        if not line:
            return line

        args = line.split()

        if args[0] in ['EOF', 'quit', 'create', 'show', 'destroy', 'all',
                       'update', 'count', 'help']:
            return line

        args = args[0].split('.')
        class_name = args[0]

        if class_name not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
            return line

        if len(args) > 1:
            args = args[1].split('(')
            command = args[0]
            obj_id = args[1].split('"')
            new_line = command + " " + class_name + " "
            if len(obj_id) > 1:
                new_line += obj_id[1]

        return new_line




if __name__ == '__main__':
    HBNBCommand().cmdloop()
