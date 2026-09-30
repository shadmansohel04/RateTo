import "../styles/about.css";

export default function aboutBody(){
    return(
        <div className="aboutBody">
            <h1>The Data</h1>
            <div className="scoreContainerTop">
                <p>Powered by <a href="https://open.toronto.ca/">OpenData Toronto</a>,
                    we utilized several comprehensive databases to create unbiased 
                    ratings for all locations in Toronto based on three key criteria: safety, transportation, 
                    and green space. Our goal was to provide Torontonians with a reliable tool to help them 
                    make informed decisions about their city. By combining data from these sources, we have 
                    developed a thorough and objective scoring system that reflects the quality of life in 
                    various neighborhoods across Toronto.
                </p>
            </div>

            <h1>The Scores</h1>

            <div className="scoreContainer">
                <h2>Safety</h2>
                <p>
                    The Safety score is determined by proximity to emergency response units, including fire stations,
                    hospitals, and police stations, as well as comprehensive crime data from the past decade. 
                    This crime data includes various types of incidents such as homicides, assaults, gun violence, 
                    and break-ins, among others. By analyzing trends over the last 10 years, we can identify which 
                    neighborhoods have consistently been safe, those that have faced challenges, and the trajectory 
                    of safety in each area. This approach allows us to provide a nuanced and accurate assessment of 
                    safety across Toronto.
                </p>
            </div>

            <div className="scoreContainer">
                <h2>Transportation</h2>
                <p>
                    The transportation score is based on several factors: the availability of rideable bike networks within 
                    a 5 km radius, the proximity of TTC stations within walking distance, and traffic data at key 
                    intersections within the neighborhood. This comprehensive evaluation ensures an accurate reflection 
                    of the convenience and accessibility of transportation options in each area.
                </p>
            </div>

            <div className="scoreContainer">
                <h2>Green Space</h2>
                <p>
                    The green space score is based on the quality of the closest park to your location, the best green 
                    space within walking distance, and proximity to aesthetic water features. This ensures that the score 
                    accurately reflects the availability and quality of natural environments in each neighborhood.
                </p>
            </div>

            <h1>Databases</h1>
            <div className="scoreContainerTop gettingDumb">
                <ul>
                    <li><a href="https://open.toronto.ca/dataset/cycling-network/">Cycling Network</a></li>
                    <li><a href="https://open.toronto.ca/dataset/neighbourhood-crime-rates/">Neighborhood Crime Rates</a></li>
                </ul>
                <ul>
                    <li><a href="https://open.toronto.ca/dataset/fire-station-locations/">Fire Stations</a></li>
                    <li><a href="https://open.toronto.ca/dataset/neighbourhood-crime-rates/">Neighborhood Crime Rates</a></li>
                </ul>

                <ul>
                    <li><a href="https://open.toronto.ca/dataset/green-spaces/">Green Spaces</a></li>
                    <li><a href="https://open.toronto.ca/dataset/police-facility-locations/">Police Stations</a></li>
                </ul>

                <ul>
                    <li><a href="https://open.toronto.ca/dataset/traffic-volumes-at-intersections-for-all-modes/">Traffic</a></li>
                </ul>

            </div>

        </div>
    )
}