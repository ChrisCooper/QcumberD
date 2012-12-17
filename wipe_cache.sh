rm $HOME/memcached.sock
memcached -d -m 64 -s $HOME/memcached.sock -P $HOME/memcached.pid 