import L from 'leaflet';

const fireURL = 'https://www.svgheart.com/wp-content/uploads/2021/11/fire-truck-emergency-vehicle-firefighter-free-svg-file-SvgHeart.Com-2.png';
const policeURL = 'https://png.pngtree.com/png-vector/20230209/ourmid/pngtree-police-car-cartoon-png-image_6592485.png'

const generic = L.icon({
    iconUrl: "https://cdn-icons-png.flaticon.com/512/25/25613.png",
    iconSize: [35, 35],
    iconAnchor: [17.5, 35],
    popupAnchor: [0, -10]
})

const fireTruck = L.icon({
    iconUrl: fireURL,
    iconSize: [35, 20],
    iconAnchor: [17, 20],
    popupAnchor: [0, -10]
});

const ttcIcon = L.icon({
    iconUrl: "https://static.thenounproject.com/png/7044-200.png",
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -10]
});

const ttcIconMain = L.icon({
    iconUrl: "https://upload.wikimedia.org/wikipedia/commons/e/e3/Logo_of_the_Toronto_Transit_Commission.svg",
    iconSize: [60, 60],
    iconAnchor: [30, 35],
    popupAnchor: [0, -10]
});

const fireTruckBig = L.icon({
    iconUrl: "https://static.vecteezy.com/system/resources/previews/019/906/515/non_2x/fire-truck-graphic-clipart-design-free-png.png",
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -10]
})

const PoliceCar = L.icon({
    iconUrl:policeURL,
    iconSize: [30, 20],
    iconAnchor: [15, 20],
    popupAnchor: [0, -10]
});

const PoliceCarClose = L.icon({
    iconUrl: "https://www.pngall.com/wp-content/uploads/15/Police-Badge-Transparent.png",
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -10]
});

const Hospitals = L.icon({
    iconUrl:"https://static.vecteezy.com/system/resources/thumbnails/017/177/954/small/round-medical-cross-symbol-on-transparent-background-free-png.png",
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -10]
})

const Hospitalclose = L.icon({
    iconUrl:"https://static.vecteezy.com/system/resources/previews/014/322/451/original/hospital-icons-design-in-blue-circle-png.png",
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -10]
})

const parkDesignClose = {
    fillColor: 'green',
    fillOpacity: 1,
    color: "green",
    weight: 2
}

const parkDesign = {
    fillColor: 'green',
    fillOpacity: 0.2,
    color: "green",
    weight: 1
}

const crimeDesign = {
    fillColor: 'blue',
    fillOpacity: 0.2,
    color: "transparent",
    weight: 0
}

const circleDesign = {
    fillColor: 'transparent',
    color: "black",
    weight: 2
}

export { 
    fireTruck, 
    fireTruckBig, 
    PoliceCar, 
    PoliceCarClose, 
    parkDesign, 
    parkDesignClose, 
    crimeDesign,
    circleDesign,
    Hospitals,
    ttcIcon,
    ttcIconMain,
    Hospitalclose,
    generic
};
