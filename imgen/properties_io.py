import os

class PropertiesIO:
    def __init__(self, path):
        """ Initialize the PropertiesIO class with the given path """
        self.path = os.path.expanduser(path)
        self.properties = {}
        self.read()
        
    
    def read(self):
        """ Read the properties from the file """
        with open(self.path, 'r') as file:
            for line in file:
                if not line.startswith('#') and '=' in line:
                    name, value = line.split('=', 1)
                    self.properties[name.strip()] = value.strip()

    def write(self):
        """ Write the properties to the file """
        with open(self.path, 'w') as file:
            for key, value in self.properties.items():
                file.write(f'{key}={value}\n')

    def get_properties(self):
        """ Get all the properties """
        return self.properties

    def get_property(self, key):
        """ Get the property with the given key """
        return self.properties.get(key)

    def set_property(self, key, value): 
        """ Set the property with the given key, value """
        self.properties[key] = value    