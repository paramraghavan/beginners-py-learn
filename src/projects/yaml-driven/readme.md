```text
Create a Singleton class in python which will 
- manage a factory class. 
- this Singleton class will manage state 
- parse yaml file using factory class
- and for each yaml action create  a new factory class  which implements a base class and perform action
```

* Create a Singleton class: This class will ensure that only one instance of it exists.
* Define a base factory class: This will be the base class for all factories.
* Implement specific factory classes: These will inherit from the base factory class and perform specific actions.
* Parse the YAML file: Use a library like PyYAML to parse the YAML file.
* Perform actions: Based on the parsed YAML content, create instances of the appropriate factory classes and perform the
  actions.