import Navbar from "./navbar";

export default function Home() {
  return (
    <div>
      <Navbar />
      <main className="text-center py-16 px-20">
        <h1 className="text-8xl font-bold text-gray-50 text-left">Find Your</h1>
        <h1 className="text-8xl font-bold text-gray-50 text-left"> <span className="text-rose-400">Muse</span>ic</h1>
        <p className="text-left text-gray-50 font-medium">
          Music information retrieval and album finder using principal component analysis.
        </p>
        <button className="mt-6 object-left px-6 py-2 bg-yellow-500 text-gray-50 font-semibold rounded-lg shadow hover:bg-yellow-600">
          View More
        </button>
        
      </main>

      <div className="bg-white py-12">
        <h2 className="text-2xl font-bold text-center">Museic Features</h2>
        <p className="text-gray-50 mb-8 text-center">Click to start</p>          
      </div>
    </div>
  );
}
