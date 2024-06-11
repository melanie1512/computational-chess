import Image from "next/image";
import Referee from './components/Referee/Referee';

function Home() {
  return (
    <main id="app" className="p-24">
      <Referee/>
    </main>
  );
}

export default Home;