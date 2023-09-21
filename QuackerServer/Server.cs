using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using System.IO;

namespace QuackerServer
{
    internal class Server
    {
        private TcpListener listener;

        public Server() { }

        public void StartServer()
        {
            listener = new TcpListener(IPAddress.Any, 65456);
            listener.Start();

            while (true)
            {
                TcpClient client = listener.AcceptTcpClient();
                NetworkStream stream = client.GetStream();
                StreamReader reader = new StreamReader(stream, Encoding.ASCII);
                StreamWriter writer = new StreamWriter(stream, Encoding.ASCII);
            }
        }
    }
}
