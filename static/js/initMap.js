let map;

async function initMap() {

    const firebaseConfig = {
        apiKey: "AIzaSyB2QcvBERc2wottjmvNsDUdFUR7JNv3-fg",
        authDomain: "ybs-gebeya.firebaseapp.com",
        databaseURL: "https://ybs-gebeya-default-rtdb.firebaseio.com",
        projectId: "ybs-gebeya",
        storageBucket: "ybs-gebeya.appspot.com",
        messagingSenderId: "772918152046",
        appId: "1:772918152046:web:6ac6c0e9b7a2e241f24f7f",
        measurementId: "G-F63WG81R52"
    };

    firebase.initializeApp(firebaseConfig);

    const locationsRef = firebase.database().ref('reg_users');
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    locationsRef.once('value', async (snapshot) => {
      const data = snapshot.val();
      const userIds = Object.keys(data);

      if (userIds.length > 0) {
        const firstUserLocation = data[userIds[0]];
        const initialCenter = {
          lat: firstUserLocation.latitude,
          lng: firstUserLocation.longitude
        };
  
        map = new Map(document.getElementById("map"), {
            zoom: 7,
            center: initialCenter,
            mapId: "DEMO_MAP_ID",
        });
  
        const {LatLngBounds} = await google.maps.importLibrary("core");
        const bounds = new LatLngBounds();

        for (const userId in data) {
            const user = data[userId];

            if (user.latitude && user.longitude && user.active) {
            const latLng = new google.maps.LatLng(user.latitude, user.longitude);

            const marker = new AdvancedMarkerElement({
                position: latLng,
                map: map,
                content: buildContent(user),
            });

            marker.addListener("click", () => {
              toggleHighlight(marker, user);
            });
        
            bounds.extend(latLng);
            }
        }
    
        map.fitBounds(bounds);
      }
    });
  }

  function toggleHighlight(markerView, property) {
    if (markerView.content.classList.contains("highlight")) {
      markerView.content.classList.remove("highlight");
      markerView.zIndex = null;
    } else {
      markerView.content.classList.add("highlight");
      markerView.zIndex = 1;
    }
  }

  function buildContent(user) {
    const content = document.createElement("div");
  
    content.innerHTML = `
      <div class="name-tag">
          ${user.name} </br> ${user.phone}
      </div>
      <div class="user">
        <div class="icon">
            <i aria-hidden="true" class="fa fa-icon fa-user" title="user"></i>
        </div>
        <div class="details">
            <div class="price">${user.phone}</div>
            <div class="address">${user.name}</div>
            <div class="features">
            <div>
                <i aria-hidden="true" class="fa fa-user-plus fa-lg user-plus" title="Users"></i>
                <span>132</span>
            </div>
            </div>
        </div>
      </div>
      `;
    return content;
  }
  

  initMap();
  