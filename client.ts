import * as net from "node:net"
import * as readline from "readline";

const client: net.Socket = new net.Socket()

const Host: string = "127.0.0.1"
const Port: number = 8080


client.connect(Port, Host, () => {
    const rl: readline.Interface= readline.createInterface({
        input: process.stdin,
        output: process.stdout
    })

    type request = {
        method: string,
        params: string|number|[number, number]|[string, string]|string[],
        param_types: string,
        id: number
    }
    const requestList: request[] = [
        {
            "method": "floor",
            "params": 7.891,
            "param_types": "double",
            "id": 0
        },
        {
            "method": "nroot",
            "params": [4,16],
            "param_types": "[int,int]",
            "id": 1
        },
        {
            "method": "reverse",
            "params": "こんにちは",
            "param_types": "string",
            "id": 2
        },
        {
            "method": "validAnagram",
            "params": ["earth","heart"],
            "param_types": "[string,string]",
            "id": 3
        },
        {
            "method": "sort",
            "params": ["こんにちは","元気","ですか"],
            "param_types": "string[]",
            "id": 4
        },
        {
            "method": "floor",
            "params": 3.1415,
            "param_types": "float",
            "id": 5
        },
        {
            "method": "subtract",
            "params": [100,58],
            "param_types": "[int,int]",
            "id": 6
        }

    ]

    console.log("Connected")
    rl.question("Please enter method: ", (method: string) => {
        const request: request | undefined = requestList.find((request: request) => request.method === method)

        if (request) {
            client.write(JSON.stringify(request))
        } else {
            console.log("Method not found in request list.")
        }
        rl.close()
    })

})

client.on("data", (data: Buffer) => {
    // type response= {
    //     result: string,
    //     result_type: string,
    //     id: number
    // }
    type request = {
        method: string,
        params: string|number|[number, number]|[string, string]|string[],
        param_types: string,
        id: number
    }
    const response: request = JSON.parse(data.toString())
    console.log("Received Data:", response)
    client.end()
    client.destroy()
})


client.on("close", () => {
    console.log("Connection closed")
})

client.on("error", (error: Error) => {
    console.log("Error:", error)
})


