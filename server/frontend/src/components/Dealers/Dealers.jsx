// server/frontend/src/components/Dealers/Dealers.jsx
import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png"

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);
  const [selectedState, setSelectedState] = useState("");

  // let root_url = window.location.origin
  const ALL_DEALERS_URL ="/djangoapp/get_dealers/";

  const fetchAllDealers = async ()=>{
    const res = await fetch(ALL_DEALERS_URL);
    const data = await res.json();
    if(data.status === 200) {
      const all_dealers = Array.from(data.dealers || []);
      setDealersList(all_dealers)
      // unique sorted list of states
      const uniqueStates = Array.from(new Set(all_dealers.map(d => d.state))).sort();
      setStates(uniqueStates);
    }
  };

  const filterDealers = async (state) => {
    const url = state && state !== "All"
        ? `/djangoapp/get_dealers/${encodeURIComponent(state)}/` 
        : ALL_DEALERS_URL

    const res = await fetch(url);
    const data = await res.json();
    if (data.status === 200) {
        setDealersList(Array.from(data.dealers || []))
    }
  };

  const onStateChange = (e) => {
    const value = e.target.value;
    setSelectedState(value);
    filterDealers(value);
  };

  useEffect(() => {
    fetchAllDealers();
  },[]);  


let isLoggedIn = sessionStorage.getItem("username") != null ? true : false;
return(
  <div>
      <Header/>

     <table className='table'>
      <tr>
      <th>ID</th>
      <th>Dealer Name</th>
      <th>City</th>
      <th>Address</th>
      <th>Zip</th>
      <th>
      <select 
        name="state" 
        id="state" 
        value={selectedState}
        onChange={onStateChange}
        >
      <option value="" disabled hidden>State</option>
      <option value="All">All States</option>
      {states.map(state => (
          <option key={state} value={state}>{state}</option>
      ))}
      </select>        

      </th>
      {isLoggedIn ? (
          <th>Review Dealer</th>
         ):<></>
      }
      </tr>
     {dealersList.map(dealer => (
        <tr key={dealer.id}>
          <td>{dealer['id']}</td>
          <td><a href={'/dealer/'+dealer['id']}>{dealer['full_name']}</a></td>
          <td>{dealer['city']}</td>
          <td>{dealer['address']}</td>
          <td>{dealer['zip']}</td>
          <td>{dealer['state']}</td>
          {isLoggedIn ? (
            <td><a href={`/postreview/${dealer['id']}`}><img src={review_icon} className="review_icon" alt="Post Review"/></a></td>
           ):<></>
          }
        </tr>
      ))}
     </table>;
  </div>
)
}

export default Dealers
