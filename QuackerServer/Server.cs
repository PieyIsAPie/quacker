using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.IO;
using System.Security.Cryptography;
using System.Runtime.InteropServices;
using System.Runtime.Remoting.Messaging;
using System.Xml.Linq;
using log4net;
using log4net.Config;
using System.Threading.Tasks;
using System.Collections.Concurrent;
using System.Xml;

namespace QuackerServer
{
    internal class Server
    {
        private static readonly ILog log = LogManager.GetLogger(typeof(Server));
        private TcpListener listener;
        static ManualResetEvent alertEvent = new ManualResetEvent(false);
        static ConcurrentQueue<string> dataQueue = new ConcurrentQueue<string>();
        static object queueLock = new object();

        public Server() { }

        public void StartServer(IPAddress address)
        {
            listener = new TcpListener(address, 65456);
            listener.Start();

            while (true)
            {
                TcpClient client = listener.AcceptTcpClient();
                NetworkStream stream = client.GetStream();
                StreamReader reader = new StreamReader(stream, Encoding.ASCII);
                StreamWriter writer = new StreamWriter(stream, Encoding.ASCII);
                char[] lineSplit = ":".ToCharArray();
                string[] request = reader.ReadLine().Split(lineSplit);
                string requestCode = request[0];
                string requestData = request[1];
                if (requestCode == "100")
                {
                    Random rnd = new Random();
                    string[] splitData = requestData.Split("-".ToCharArray());
                    string name = splitData[0];
                    string color = splitData[1];
                    long id = (long)(rnd.NextDouble() * (99999999999999999L - 10000000000000000L) + 10000000000000000L);
                    writer.WriteLine("200: {0}", id.ToString());
                    writer.Flush();
                    var data = (reader, writer, client, name, color, id);
                    Task.Run(() => HandleClient(data));
                }
            }
        }
        static async Task HandleClient(object data)
        {
            await Task.WhenAll(WaitForEvent(data), WaitForClientRequest(data));

        }
        static async Task WaitForEvent(object data)
        {
            var (reader, writer, client, name, color, id) = ((StreamReader, StreamWriter, TcpClient, string, string, long))data;
            while (true)
            {
                alertEvent.WaitOne();
                string item;
                while (dataQueue.TryDequeue(out item))
                {
                    if (item.Contains("302: "))
                    await writer.WriteLineAsync($"202: {item}-{name}-{color}-{id}");
                    await writer.FlushAsync();
                }
            }

        }

        static async Task WaitForClientRequest(object data)
        {
            var (reader, writer, client, name, color, id) = ((StreamReader, StreamWriter, TcpClient, string, string, long))data;
            while (true)
            {
                var request = reader.ReadLine();
            }
            
        }
        static void ProduceMessage(string data)
        {
            lock (queueLock)
            {
                dataQueue.Enqueue(data);
            }
        }
    }
}
