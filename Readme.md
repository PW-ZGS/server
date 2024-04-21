Description of the project:

This project is a backend for a carpooling application that facilitates ride-sharing among employees. The platform aims to connect individuals traveling along similar routes and at similar times, optimizing their commutes and reducing transportation costs.

Key functionalities:

    Trip creation: Employees can create new trips specifying their starting point, destination, date and time of departure, and maximum number of passengers.
    Route requests: Individuals interested in joining a ride can submit route requests indicating their starting point, destination, and preferred departure time.
    Matching algorithm: The system utilizes an OpenStreetMap-based algorithm to find optimal routes and match drivers with passengers with similar routes and departure times.
    Match generation: Upon identifying suitable driver-passenger pairs, the system generates matches, providing drivers with passengers' contact information to connect and arrange ride details.

Benefits:

    Time and cost savings: Carpooling enables reduced fuel and parking expenses, as well as time saved from traffic congestion.
    Reduced CO2 emissions: Shared rides contribute to lowering tailpipe emissions and protecting the environment.
    Improved communication and integration: The platform facilitates employee connections and fosters team bonding.

Technology:

    Backend: Python, FastAPI framework
    Cloud: AWS, Kubernetes
    Database: PostgreSQL
    Matching algorithm: OpenStreetMap, distance and travel time-based matching algorithm
    Communication: REST API

Additional notes:

    The project is under active development and continuous improvement.
    Customization of functionalities to suit specific company needs is possible.
    API documentation is available online.

Infrastructure descirpition:
    
    We have EC2 based Kubernetes cluster stored on AWS. Cluster consists of 3 nodes. Server is packed to docker image and is sent to dockerhub. 
    Further this image is pulled in Kubernetes cluster and sufficient deployment and network routes are created. Database also is stored in 
    this Kubernetes cluster. This architecture is very cheap, so it's worth to use it in small companies.


Openapi spec: https://app.swaggerhub.com/apis/MrPickle311/hackaton/1.0.0
