CREATE DATABASE destinations;

USE destinations;

CREATE TABLE countries (
country_code VARCHAR(5) NOT NULL Primary Key,
country_name VARCHAR(50) NOT NULL);

INSERT INTO countries (
country_code, country_name)
VALUES
("us", "United States"),
("ca", "Canada"),
("gb", "United Kingdom"),
("aus", "Australia"),
("fr", "France"),
("de", "Germany"),
("it", "Italy"),
("es", "Spain"),
("nl", "Netherlands"),
("se", "Sweden"),
("no", "Norway"),
("dk", "Denmark"),
("fi", "Finland"),
("ie", "Ireland"),
("ch", "Switzerland"),
("at", "Austria"),
("be", "Belgium"),
("cz", "Czech Republic"),
("pl", "Poland"),
("hu", "Hungary"),
("ro", "Romania"),
("bg", "Bulgaria"),
("gr", "Greece"),
("tr", "Turkey"),
("il", "Israel"),
("ae", "United Arab Emirates"),
("sa", "Saudi Arabia"),
("in", "India"),
("jp", "Japan"),
("cn", "China"),
("kr", "South Korea"),
("my", "Malaysia"),
("th", "Thailand"),
("ph", "Philippines"),
("vn", "Vietnam"),
("id", "Indonesia"),
("au", "Australia"),
("nz", "New Zealand"),
("za", "South Africa"),
("eg", "Egypt"),
("ma", "Morocco"),
("dz", "Algeria"),
("tn", "Tunisia"),
("ke", "Kenya"),
("ng", "Nigeria"),
("gh", "Ghana"),
("ci", "Ivory Coast"),
("zw", "Zimbabwe"),
("tz", "Tanzania"),
("pe", "Peru"),
("br", "Brazil"),
("ar", "Argentina"),
("cl", "Chile"),
("co", "Colombia"),
("uy", "Uruguay"),
("bo", "Bolivia"),
("py", "Paraguay"),
("ec", "Ecuador"),
("pt", "Portugal"),
("do", "Dominican Republic"),
("ht", "Haiti"),
("jm", "Jamaica"),
("bs", "Bahamas"),
("ag", "Antigua and Barbuda"),
("lc", "Saint Lucia"),
("gd", "Grenada"),
("kn", "Saint Kitts and Nevis"),
("tt", "Trinidad and Tobago"),
("vg", "British Virgin Islands"),
("tc", "Turks and Caicos Islands"),
("bb", "Barbados"),
("sg", "Singapore"),
("hk", "Hong Kong"),
("tw", "Taiwan"),
("mx", "Mexico");

CREATE TABLE cities (
id INT NOT NULL Primary Key,
country_code VARCHAR(5) NOT NULL,
city_name VARCHAR(50) NOT NULL,
keyword VARCHAR(50) NOT NULL,
CONSTRAINT fk_code
FOREIGN KEY (country_code)
REFERENCES countries(country_code));

INSERT INTO cities (
id, country_code, city_name, keyword)
VALUES
    (123456, "us", "New York", "history"),
    (123457, "us", "Los Angeles", "beaches"),
    (123458, "us", "San Francisco", "history"),
    (123459, "us", "Chicago", "history"),
    (123460, "ca", "Toronto", "museums"),
    (123461, "ca", "Vancouver", "beaches"),
    (123462, "ca", "Montreal", "history"),
    (123463, "ca", "Calgary", "mountains"),
    (123464, "gb", "London", "museums"),
    (123465, "gb", "Edinburgh", "history"),
    (123466, "gb", "Manchester", "theatre"),
    (123467, "gb", "Liverpool", "museums"),
    (123468, "aus", "Sydney", "beaches"),
    (123469, "aus", "Melbourne", "museums"),
    (123470, "aus", "Brisbane", "beaches"),
    (123471, "aus", "Perth", "beaches"),
    (123472, "fr", "Paris", "museums"),
    (123473, "fr", "Nice", "beaches"),
    (123474, "fr", "Lyon", "history"),
    (123475, "fr", "Bordeaux", "wine"),
    (123476, "de", "Berlin", "museums"),
    (123477, "de", "Munich", "history"),
    (123478, "de", "Frankfurt", "museums"),
    (123479, "de", "Hamburg", "history"),
    (123480, "it", "Rome", "history"),
    (123481, "it", "Venice", "history"),
    (123482, "it", "Florence", "history"),
    (123483, "it", "Milan", "fashion"),
    (123484, "es", "Madrid", "museums"),
    (123485, "es", "Barcelona", "beaches"),
    (123486, "es", "Seville", "history"),
    (123487, "es", "Valencia", "beaches"),
    (123488, "nl", "Amsterdam", "museums"),
    (123489, "nl", "Rotterdam", "modern"),
    (123490, "nl", "Utrecht", "history"),
    (123491, "nl", "Hague", "history"),
    (123492, "se", "Stockholm", "museums"),
    (123493, "se", "Gothenburg", "museums"),
    (123494, "se", "Malmo", "history"),
    (123495, "se", "Uppsala", "history"),
    (123496, "no", "Oslo", "museums"),
    (123497, "no", "Bergen", "history"),
    (123498, "no", "Stavanger", "beaches"),
    (123499, "no", "Trondheim", "history"),
    (123500, "dk", "Copenhagen", "museums"),
    (123501, "dk", "Aarhus", "history"),
    (123502, "dk", "Odense", "history"),
    (123503, "dk", "Aalborg", "history"),
    (123504, "fi", "Helsinki", "museums"),
    (123505, "fi", "Espoo", "history"),
    (123506, "fi", "Tampere", "museums"),
    (123507, "fi", "Oulu", "history"),
    (123508, "ie", "Dublin", "museums"),
    (123509, "ie", "Cork", "history"),
    (123510, "ie", "Galway", "history"),
    (123511, "ie", "Limerick", "history"),
    (123512, "ch", "Zurich", "museums"),
    (123513, "ch", "Geneva", "history"),
    (123514, "ch", "Bern", "history"),
    (123515, "ch", "Lausanne", "museums"),
    (123516, "at", "Vienna", "museums"),
    (123517, "at", "Salzburg", "history"),
    (123518, "at", "Innsbruck", "mountains"),
    (123519, "at", "Graz", "history"),
    (123520, "be", "Brussels", "museums"),
    (123521, "be", "Antwerp", "fashion"),
    (123522, "be", "Ghent", "history"),
    (123523, "be", "Bruges", "history"),
    (123524, "cz", "Prague", "history"),
    (123525, "cz", "Brno", "history"),
    (123526, "cz", "Plzen", "history"),
    (123527, "cz", "Olomouc", "history"),
    (123528, "pl", "Warsaw", "history"),
    (123529, "pl", "Krakow", "history"),
    (123530, "pl", "Wroclaw", "history"),
    (123531, "pl", "Gdansk", "history"),
    (123532, "hu", "Budapest", "history"),
    (123533, "hu", "Debrecen", "history"),
    (123534, "hu", "Szeged", "history"),
    (123535, "hu", "Pecs", "history"),
    (123536, "ro", "Bucharest", "history"),
    (123537, "ro", "Cluj-Napoca", "history"),
    (123538, "ro", "Timisoara", "history"),
    (123539, "ro", "Brasov", "history"),
    (123540, "bg", "Sofia", "history"),
    (123541, "bg", "Plovdiv", "history"),
    (123542, "bg", "Varna", "beaches"),
    (123543, "bg", "Burgas", "beaches"),
    (123544, "gr", "Athens", "history"),
    (123545, "gr", "Thessaloniki", "history"),
    (123546, "gr", "Heraklion", "beaches"),
    (123547, "gr", "Rhodes", "beaches"),
    (123548, "tr", "Istanbul", "history"),
    (123549, "tr", "Cappadocia", "tourism"),
    (123550, "tr", "Antalya", "beaches"),
    (123551, "tr", "Izmir", "history"),
    (123552, "il", "Tel Aviv", "beaches"),
    (123553, "il", "Jerusalem", "history"),
    (123554, "il", "Haifa", "history"),
    (123555, "il", "Eilat", "beaches"),
    (123556, "ae", "Dubai", "beaches"),
    (123557, "ae", "Abu Dhabi", "museums"),
    (123558, "ae", "Sharjah", "museums"),
    (123559, "ae", "Ajman", "beaches"),
    (123560, "sa", "Riyadh", "history"),
    (123561, "sa", "Jeddah", "beaches"),
    (123562, "sa", "Dammam", "beaches"),
    (123563, "sa", "Mecca", "history"),
    (123564, "in", "New Delhi", "museums"),
    (123565, "in", "Mumbai", "history"),
    (123566, "in", "Bangalore", "museums"),
    (123567, "in", "Chennai", "history"),
    (123568, "jp", "Tokyo", "museums"),
    (123569, "jp", "Kyoto", "history"),
    (123570, "jp", "Osaka", "history"),
    (123571, "jp", "Hiroshima", "history"),
    (123572, "cn", "Beijing", "history"),
    (123573, "cn", "Shanghai", "museums"),
    (123574, "cn", "Xi'an", "history"),
    (123575, "cn", "Guangzhou", "history"),
    (123576, "kr", "Seoul", "museums"),
    (123577, "kr", "Busan", "beaches"),
    (123578, "kr", "Incheon", "beaches"),
    (123579, "kr", "Jeju", "beaches"),
    (123580, "my", "Kuala Lumpur", "museums"),
    (123581, "my", "Penang", "beaches"),
    (123582, "my", "Langkawi", "beaches"),
    (123583, "my", "Malacca", "history"),
    (123584, "th", "Bangkok", "museums"),
    (123585, "th", "Chiang Mai", "history"),
    (123586, "th", "Phuket", "beaches"),
    (123587, "th", "Krabi", "beaches"),
    (123588, "ph", "Manila", "museums"),
    (123589, "ph", "Cebu City", "beaches"),
    (123590, "ph", "Davao City", "beaches"),
    (123591, "ph", "Iloilo City", "beaches"),
    (123592, "vn", "Hanoi", "history"),
    (123593, "vn", "Ho Chi Minh City", "history"),
    (123594, "vn", "Da Nang", "beaches"),
    (123595, "vn", "Nha Trang", "beaches"),
    (123596, "id", "Bali", "beaches"),
    (123597, "id", "Jakarta", "museums"),
    (123598, "id", "Yogyakarta", "history"),
    (123599, "id", "Surabaya", "history"),
    (123600, "au", "Sydney", "beaches"),
    (123601, "au", "Melbourne", "museums"),
    (123602, "au", "Brisbane", "beaches"),
    (123603, "au", "Perth", "beaches"),
    (123604, "nz", "Auckland", "museums"),
    (123605, "nz", "Wellington", "museums"),
    (123606, "nz", "Christchurch", "history"),
    (123607, "nz", "Queenstown", "mountains"),
    (123608, "za", "Cape Town", "beaches"),
    (123609, "za", "Johannesburg", "history"),
    (123610, "za", "Durban", "beaches"),
    (123611, "za", "Pretoria", "history"),
    (123612, "eg", "Cairo", "history"),
    (123613, "eg", "Alexandria", "history"),
    (123614, "eg", "Luxor", "history"),
    (123615, "eg", "Aswan", "history"),
    (123616, "ma", "Marrakech", "history"),
    (123617, "ma", "Casablanca", "history"),
    (123618, "ma", "Fes", "history"),
    (123619, "ma", "Tangier", "history"),
    (123620, "dz", "Algiers", "history"),
    (123621, "dz", "Oran", "history"),
    (123622, "dz", "Constantine", "history"),
    (123623, "dz", "Annaba", "history"),
    (123624, "tn", "Tunis", "history"),
    (123625, "tn", "Sousse", "beaches"),
    (123626, "tn", "Hammamet", "beaches"),
    (123627, "tn", "Sfax", "history"),
    (123628, "ke", "Nairobi", "museums"),
    (123629, "ke", "Mombasa", "beaches"),
    (123630, "ke", "Kisumu", "history"),
    (123631, "ke", "Nakuru", "history"),
    (123632, "ng", "Lagos", "beaches"),
    (123633, "ng", "Abuja", "history"),
    (123634, "ng", "Port Harcourt", "history"),
    (123635, "ng", "Kano", "history"),
    (123636, "gh", "Accra", "history"),
    (123637, "gh", "Kumasi", "history"),
    (123638, "gh", "Takoradi", "history"),
    (123639, "gh", "Tamale", "history"),
    (123640, "ci", "Abidjan", "history"),
    (123641, "ci", "Yamoussoukro", "history"),
    (123642, "ci", "San Pedro", "history"),
    (123643, "ci", "Bouake", "history"),
    (123644, "zw", "Harare", "history"),
    (123645, "zw", "Bulawayo", "history"),
    (123646, "zw", "Victoria Falls", "tourism"),
    (123647, "zw", "Gweru", "history"),
    (123648, "tz", "Dar es Salaam", "beaches"),
    (123649, "tz", "Zanzibar City", "beaches"),
    (123650, "tz", "Arusha", "mountains"),
    (123651, "tz", "Dodoma", "history"),
    (123652, "pe", "Lima", "museums"),
    (123653, "pe", "Cusco", "history"),
    (123654, "pe", "Arequipa", "history"),
    (123655, "pe", "Trujillo", "history"),
    (123656, "br", "Rio de Janeiro", "beaches"),
    (123657, "br", "Sao Paulo", "museums"),
    (123658, "br", "Salvador", "history"),
    (123659, "br", "Brasilia", "history"),
    (123660, "ar", "Buenos Aires", "theatre"),
    (123661, "ar", "Cordoba", "history"),
    (123662, "ar", "Mendoza", "mountains"),
    (123663, "ar", "Rosario", "history"),
    (123664, "cl", "Santiago", "history"),
    (123665, "cl", "Valparaiso", "history"),
    (123666, "cl", "Concepcion", "history"),
    (123667, "cl", "La Serena", "history"),
    (123668, "co", "Bogota", "museums"),
    (123669, "co", "Medellin", "history"),
    (123670, "co", "Cartagena", "beaches"),
    (123671, "co", "Cali", "history"),
    (123672, "uy", "Montevideo", "beaches"),
    (123673, "uy", "Punta del Este", "beaches"),
    (123674, "uy", "Salto", "history"),
    (123675, "uy", "Colonia del Sacramento", "history"),
    (123676, "bo", "La Paz", "history"),
    (123677, "bo", "Santa Cruz", "history"),
    (123678, "bo", "Sucre", "history"),
    (123679, "bo", "Cochabamba", "history"),
    (123680, "py", "Asuncion", "history"),
    (123681, "py", "Ciudad del Este", "history"),
    (123682, "py", "Encarnacion", "history"),
    (123683, "py", "Concepcion", "history"),
    (123684, "ec", "Quito", "history"),
    (123685, "ec", "Guayaquil", "history"),
    (123686, "ec", "Cuenca", "history"),
    (123687, "ec", "Banos", "tourism"),
    (123688, "pt", "Porto", "wine"),
    (123689, "pt", "Lisbon", "history"),
    (123690, "pt", "Sintra", "mountains"),
    (123691, "pt", "Aveiro", "history"),
    (123692, "do", "Santo Domingo", "history"),
    (123693, "do", "Punta Cana", "beaches"),
    (123694, "do", "Puerto Plata", "beaches"),
    (123695, "do", "Santiago", "history"),
    (123696, "ht", "Port-au-Prince", "history"),
    (123697, "ht", "Cap-Haotien", "history"),
    (123698, "ht", "Jacmel", "history"),
    (123699, "ht", "Les Cayes", "history"),
    (123700, "jm", "Kingston", "history"),
    (123701, "jm", "Montego Bay", "beaches"),
    (123702, "jm", "Ocho Rios", "beaches"),
    (123703, "jm", "Negril", "beaches"),
    (123704, "bs", "Nassau", "beaches"),
    (123705, "bs", "Freeport", "beaches"),
    (123706, "bs", "Andros Town", "beaches"),
    (123707, "bs", "Eleuthera", "beaches"),
    (123709, "ag", "English Harbour", "beaches"),
    (123710, "ag", "Jolly Harbour", "beaches"),
    (123711, "ag", "Falmouth", "beaches"),
    (123712, "lc", "Castries", "beaches"),
    (123713, "lc", "Gros Islet", "beaches"),
    (123714, "lc", "Soufriere", "beaches"),
    (123715, "lc", "Vieux Fort", "beaches"),
    (123717, "gd", "Grand Anse", "beaches"),
    (123718, "gd", "Sauteurs", "beaches"),
    (123719, "gd", "Carriacou", "beaches"),
    (123720, "kn", "Basseterre", "beaches"),
    (123721, "kn", "Frigate Bay", "beaches"),
    (123722, "kn", "Charlestown", "beaches"),
    (123723, "kn", "Newtown", "beaches"),
    (123724, "tt", "Port of Spain", "museums"),
    (123725, "tt", "San Fernando", "history"),
    (123726, "tt", "Scarborough", "history"),
    (123727, "tt", "Chaguanas", "history"),
    (123728, "vg", "Road Town", "beaches"),
    (123729, "vg", "Tortola", "beaches"),
    (123730, "vg", "Virgin Gorda", "beaches"),
    (123731, "vg", "Jost Van Dyke", "beaches"),
    (123732, "tc", "Grand Turk", "beaches"),
    (123733, "tc", "Providenciales", "beaches"),
    (123734, "tc", "North Caicos", "beaches"),
    (123735, "tc", "Middle Caicos", "beaches"),
    (123736, "bb", "Bridgetown", "beaches"),
    (123737, "bb", "Oistins", "beaches"),
    (123738, "bb", "Speightstown", "beaches"),
    (123739, "bb", "Holetown", "beaches"),
    (123740, "sg", "Singapore", "museums"),
    (123741, "sg", "Sentosa", "beaches"),
    (123742, "sg", "Orchard Road", "shopping"),
    (123743, "sg", "Marina Bay", "museums"),
    (123744, "hk", "Hong Kong", "museums"),
    (123745, "hk", "Kowloon", "museums"),
    (123746, "hk", "Causeway Bay", "shopping"),
    (123747, "hk", "Tsim Sha Tsui", "museums"),
    (123748, "tw", "Taipei", "museums"),
    (123749, "tw", "Kaohsiung", "history"),
    (123750, "tw", "Taichung", "history"),
    (123751, "tw", "Tainan", "history"),
    (123752, "mx", "Cancun", "beaches"),
    (123753, "mx", "Mexico City", "museums"),
    (123754, "mx", "Taxco", "history");


CREATE TABLE favourite_hotels (
fav_hotel_ID INT NOT NULL Primary Key,
hotel_name VARCHAR(50) NOT NULL,
city_ID INT NOT NULL,
country_code VARCHAR(5) NOT NULL,
favourited_date DATE,
CONSTRAINT fk_country_code
FOREIGN KEY (country_code)
REFERENCES countries(country_code),
FOREIGN KEY (city_ID)
REFERENCES cities(id));

INSERT INTO favourite_hotels (
fav_hotel_ID, hotel_name, city_ID, country_code, favourited_date)
VALUES
("89176", "Shangri-La Toronto", '123460', "ca", '2024-08-23');


CREATE TABLE favourite_activities (
activity_ID VARCHAR(10) NOT NULL Primary Key,
activity_name VARCHAR(50) NOT NULL,
city_ID INT NOT NULL,
country_code VARCHAR(5) NOT NULL,
favourited_date DATE,
CONSTRAINT fk_country_codes
FOREIGN KEY (country_code)
REFERENCES countries(country_code),
FOREIGN KEY (city_ID)
REFERENCES cities(id));

INSERT INTO favourite_activities (
activity_ID, activity_name, city_ID, country_code, favourited_date)
VALUES
('Q60749334', "LEGOLAND Discovery Centre Toronto", '123460', "ca", '2024-08-23');