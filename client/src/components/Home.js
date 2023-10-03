import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Home() {
  const [heros, setHeros] = useState([]);

  useEffect(() => {
    fetch("/heroes")
      .then((r) => {
        if(!r.ok){
          throw new Error(`Network response was not ok: ${r.status}`)
        }
        return r.json()
      })
        
      .then((data) =>{
        setHeros(data)
      });
       
  }, []);

  return (
    <section>
      <h2>All Heroes</h2>
      <ul>
        {heros.map((hero) => (
          <li key={hero.id}>
            <Link to={`/heroes/${hero.id}`}>{hero.super_name}</Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default Home;
