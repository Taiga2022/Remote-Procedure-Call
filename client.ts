import * as net from "node:net"

const client: net.Socket = new net.Socket()

const Host: string = "127.0.0.1"
const Port: number = 8080

client.connect(Port, Host, () => {
    console.log("Connected")

    client.write("Hello World!")
})

client.on("data", (data: Buffer) => {
    console.log("Received Data:", data.toString())
    client.end()
    client.destroy()
})


client.on("close", () => {
    console.log("Connection closed")
})

client.on("error", (error: Error) => {
    console.log("Error:", error)
})
