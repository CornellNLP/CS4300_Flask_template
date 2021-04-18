import axios from 'axios';
import getEnvVars from '../environment';
const { yelpFusionKey } = getEnvVars();

const instance = axios.create({
    baseURL: "https://api.yelp.com/v3",
    headers:{
        Authorization: `Bearer ${yelpFusionKey}`
    }
})

export default instance;