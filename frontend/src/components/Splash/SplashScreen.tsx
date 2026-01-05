import loading from "../../assets/loading.svg";

export default function Loading() {
    return (
        <div
        style={{
            backgroundColor: "#fff",
            width: "100%",
            height: "100%",
            position: "fixed",
            top: 0,
            left: 0,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            overflow: "hidden",
            zIndex: 1000,
        }}
    >
        <div className="animate-pulse z-50">
           <p>BYN-AI powered Ticketing  System</p>
        </div>
    </div>
    );
}
