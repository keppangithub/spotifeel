export default function PlaylistForm() {
    const [name, setName] = useState("");
    const [number, setNumber] = useState("");
    const [description, setDescription] = useState("");

    const sendData = async () => {
        const response = await fetch("http://localhost:5000/playlists", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, number: parseInt(number), description })
        });

        const data = await response.json();
        console.log("Response:", data);

        if (response.ok) {
            alert("Spellista skapad!");
        } else {
            alert("Fel: " + data.error);
        }
    };

    return(
        {
            "Test" : "Hej"
        }
    );
}
