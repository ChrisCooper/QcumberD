rm $HOME/memcached.sock
rm $HOME/memcached.pid
memcached -d -m 64 -s $HOME/memcached.sock -P $HOME/memcached.pid 
