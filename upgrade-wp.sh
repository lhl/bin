#!/bin/bash

# WP dir
echo "==="
echo "Starting upgrade..."
echo "==="
cd /home/lhl/www/randomfoo.net/htdocs

# Backup
echo ""
echo "==="
echo "Backing up..."
echo "==="
tar cvfz ~/backup/wp.old.tgz wp
mysqldump wp | gzip > ~/backup/wp.sql.gz

# Newest version
echo ""
echo "==="
echo "Getting latest version of WP..."
echo "==="
wget http://wordpress.org/latest.tar.gz
tar xvfz latest.tar.gz

# Fixups
echo ""
echo "==="
echo "Importing wp-config and wp-content..."
echo "==="
rm -rf wordpress/wp-content
cp wp/.htaccess wordpress/.htaccess
cp wp/wp-config.php wordpress/wp-config.php
cp -a wp/wp-content wordpress/wp-content

# Swap
echo ""
echo "==="
echo "Swapping to new version!"
echo "==="
mv wp wp.old
mv wordpress wp

echo ""
echo "==="
echo -n "Test your new WP.  Does it work (y/n): "
read works

if [ "$works" == "y" ]; then
  echo ""
  echo "==="
  echo "Great! Cleaning up."
  echo "==="
  rm -rf wp.old
  rm latest.tar.gz
else
  mv wp wordpress
  mv wp.old wp
  echo ""
  echo "==="
  echo "Reverted folder move.  Check to see what's wrong!"
  echo "==="
fi
