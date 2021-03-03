import javax.print.attribute.standard.PrintQuality;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.util.Arrays;

public class JavaUdpServer {

    public static void main(String args[])
    {
        System.out.println("JAVA UDP SERVER");
        DatagramSocket socket = null;
        int portNumber = 9008;

        try{
            socket = new DatagramSocket(portNumber);
            byte[] receiveBuffer = new byte[1024];

            while(true) {
                Arrays.fill(receiveBuffer, (byte)0);
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);

                //########### EX1/2
                //
                //
//                String msg = new String(receivePacket.getData());
//                System.out.println("received msg: " + msg);
//                //get client address and port to be able to send response
//                InetAddress clientAddress = receivePacket.getAddress();
//                int clientPort = receivePacket.getPort();
//                byte[] sendBuffer = "Pong Java Udp".getBytes();
//                DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, clientAddress, clientPort);
//                socket.send(sendPacket);
                //
                //
                //###########

                //########### EX3
                //
                //
//                int receivedNumber = ByteBuffer.wrap(receivePacket.getData()).getInt();
//                System.out.println("received msg: " + receivedNumber);
//                InetAddress clientAddress = receivePacket.getAddress();
//                int clientPort = receivePacket.getPort();
//
//                byte[] sendBuffer = ByteBuffer.allocate(4).putInt(receivedNumber + 1).array();
//                DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, clientAddress, clientPort);
//                socket.send(sendPacket);
                //
                //
                //###########

                //########### EX4
                //
                //
                var data = receivePacket.getSocketAddress();
                var clientAddress = receivePacket.getSocketAddress();
                System.out.println("received msg: " + (data));

                byte[] sendBuffer = "Got you ;)".getBytes();
                DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, clientAddress);
                socket.send(sendPacket);
                //
                //
                //###########

            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
        finally {
            if (socket != null) {
                socket.close();
            }
        }
    }
}
